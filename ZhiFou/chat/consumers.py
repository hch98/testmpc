from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import connection,models
from .models import Message


# 一个客户端就是一个consumer
class ChatConsumer(AsyncJsonWebsocketConsumer):

    # 连接处理函数，客户端建立WebSocket连接时，
    # 将Consumer实例加入组
    # room_group_name 组名
    # channel_name Consumer实例的channel名字
    # 连接成功之后返回该用户与聊天对象的聊天记录
    # json格式如下：
    # {
    #     "sequence_id": 聊天记录序列号,方便用来排序
    #     "from_id": 发送者id
    #     "to_id": 接收者id
    #     "role": 0(或者1) 主要用于方便前端判断这条消息发送者是否是本人
    #     "create_time": 发送消息的时间
    #     "content": 消息内容
    # }
    async def connect(self):

        #将url上from_id、to_id组成房间名，并且按照id从小到大组合
        # self.group_name = self.scope['url_route']['kwargs']['group_name']
        from_id = self.scope['url_route']['kwargs']['from_id']
        to_id = self.scope['url_route']['kwargs']['to_id']
        if from_id < to_id:
            self.room_name = from_id+'-'+to_id
        else:
            self.room_name = to_id+'-'+from_id
        self.room_group_name = 'chat_%s' % self.room_name

        #将from_id添加到类实例成员变量
        self.id = from_id

        #将该用户实例加入到channel
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 启动WebSocket连接
        await self.accept()
     
        #获取聊天记录,后续优化可以封装此代码，用于优化
        cursor = connection.cursor()
        cursor.execute(
            'select sequence_id,from_id,to_id,chat_send_time,chat_content from tb_message where from_id= %s and to_id=%s ' \
            'and to_days(chat_send_time) = to_days(now()) union select sequence_id,from_id,to_id,chat_send_time,chat_content ' \
            'from tb_message where from_id = %s and to_id = %s and to_days(chat_send_time) = to_days(now()) order by sequence_id DESC'\
            ,[from_id,to_id,to_id,from_id]
        )
        messages = cursor.fetchall()
        if len(messages):
            json_list = []
            for message in messages:        
                #发送方是自己
                if message[1]==from_id:
                    json_dict = {
                        "sequence_id": message[0],
                        "from_id": message[1],
                        "to_id": message[2],
                        "role":1,
                        "create_time": message[3].strftime('%Y-%m-%d %H: %M: %S '),
                        "content": message[4],
                    }
                #发送方是对方
                else:
                    json_dict = {
                        "sequence_id": message[0],
                        "from_id": message[1],
                        "to_id": message[2],
                        "role":0,
                        "create_time": message[3].strftime('%Y-%m-%d %H: %M: %S '),
                        "content": message[4],
                    }
                json_list.append(json_dict)

            #self.send_json()效果为发送消息给自己
            await self.send_json(json_list)


    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # 将该客户端移除聊天组连接信息
        # ChatConsumer.session[self.room_group_name].remove(self)
        await self.close()

    async def receive_json(self, message, **kwargs):
        # 收到信息时调用,持久化聊天记录
        to_id = message.get('to_id')
        from_id = message.get('from_id')
        chat_send_time = message.get('create_time')
        chat_content = message.get('content')
        Message_temp = Message(from_id=from_id,to_id=to_id,chat_content=chat_content,chat_send_time=chat_send_time)
        Message_temp.save()

        # 信息发送到群组里面,以json格式发送数据
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                #这里"type"的值中.会换成_ 在本Consumer寻找chat_message()这个方法
                "type": "chat.message",
                "content": chat_content,
                "from_id": from_id,
                "to_id": to_id,
                "create_time": chat_send_time,
            },
        )

    async def chat_message(self, event):

        #发送方是自己
        from_id = event["from_id"]
        if from_id == self.id:
            await self.send_json({
                "content": event["content"],
                "from_id": event["from_id"],
                "to_id": event["to_id"],
                "role" : 1,
                "create_time": event["create_time"],
            })
        else:
            await self.send_json({
                "content": event["content"],
                "from_id": event["from_id"],
                "to_id": event["to_id"],
                "role" : 0,
                "create_time": event["create_time"],
            })
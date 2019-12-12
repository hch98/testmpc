# chat/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect, request, HttpResponse
from django.utils.safestring import mark_safe
import json

# def index(request):
#     return render(request, 'chat/index.html', {})

def room(request,from_id,to_id):
    return render(request, 'chat/room.html', {
        'from_id': from_id,
        'to_id':to_id,
    })

#获得聊天记录接口
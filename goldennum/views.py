import json
import random
import os

from django.shortcuts import render
from django.http import HttpResponse

import secretkey
from . import datamaker

from goldennum.models import *
# Create your views here.

def getAct(request):
    retjson = datamaker.randomUsers()
    try:
        if request.GET['key'] == secretkey.secretKey:
            print("Get getAct from room %s" % (request.GET['roomid']))
            return HttpResponse(json.dumps(retjson))
        else:
            return HttpResponse("Certification failed")
    except:
        return HttpResponse("Invalid request") 


def submitResult(request):
    try:
        if request.GET['key'] == secretkey.secretKey:
            print("Get submitResult from room %s" % (request.GET['roomid']))
            result = json.loads(request.body)
            return HttpResponse("OK")
        else:
            return HttpResponse("Certification failed")            
    except:
        return HttpResponse("Invalid request")

def startRoom(request):
    try:
        if request.GET['key'] == secretkey.secretKey:

            newRoom = Room()
            try:
                Room.objects.get(roomid=request.GET['roomid'])
                return HttpResponse("Room alright exist")
            except:
                pass

            newRoom.roomid = request.GET['roomid']
            newRoom.time = int(request.GET['time'])
            newRoom.history = json.dumps([])

            cmd = "python3 plug-ins/goldennum.py " + secretkey.secretKey + " " + request.GET['roomid'] + " " + request.GET['time']
            cmd_run = "nohup " + cmd + " &"
            cmd_kill = 'pkill -f "' + cmd + '"'
            # os.system(cmd_run)

            newRoom.cmd_run = cmd_run
            newRoom.cmd_kill = cmd_kill
            newRoom.save()
            return HttpResponse("success")
        else:
            HttpResponse("Certification failed")
    except:
        return HttpResponse("Invalid request")

def stopRoom(request):
    try:
        if request.GET['key'] == secretkey.secretKey:
            pass
        else:
            pass
    except:
        HttpResponse("Invalid request")
    return HttpResponse("fuck")
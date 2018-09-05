import json
import random
import os
import time

from django.shortcuts import render
from django.http import HttpResponse

import secretkey
from . import datamaker

from goldennum.models import User, Room
# Create your views here.

def userReg(request):
    try:
        name = request.GET['name']
    except:
        return HttpResponse("Invalid request")

    if request.session.get("name") is None:
        if len(User.objects.filter(name=name)) != 0:
            return HttpResponse("User exist")
        else:
            newUser = User()
            newUser.name = name
            newUser.room = ""
            newUser.score = "0"
            newUser.act = ""
            newUser.save()
            request.session['name'] = name
            return HttpResponse("User register success")
    else:
        return HttpResponse("User have logged in")
    

def userOut(request):
    try:
        del request.session['name']
        return HttpResponse("Logged out")
    except:
        return HttpResponse("No login")

def userAct(request):
    try:
        name = request.session['name']
    except:
        return HttpResponse("No login")

    try:
        roomid = request.GET['roomid']
        num1 = float(request.GET['num1'])
        num2 = float(request.GET['num2'])
        if num1 > 100 or num1 < 0 or num2 > 100 or num2 < 0:
            return HttpResponse("Numbers overflow")
    except:
        return HttpResponse("Invalid request")

    try:
        user = User.objects.filter(name=name).filter(room=roomid)[0]
        print("old")
    except:
        user = User()
        user.name = name
        user.room = roomid
        user.score = "0"
        print("new")

    user.act = str(num1) + " " + str(num2)
    user.save()

    return HttpResponse("Upload success")

def getAct(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        return HttpResponse("Invalid request")

    if key != secretkey.secretKey:
        return HttpResponse("Certification failed")
    
    # retjson = datamaker.randomUsers()
    print("Get getAct from room %s" % (roomid))
    users = User.objects.filter(room=roomid)
    retjson = {
        "userNum": 2,
        "users": [
            {
                "userName": "fuck1",
                "userAct": [1, 2]
            },
            {
                "userName": "fuck2",
                "userAct": [3, 4]
            }
        ]
    }
    return HttpResponse(json.dumps(retjson))

def submitResult(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        return HttpResponse("Invalid request")

    if key != secretkey.secretKey:
        return HttpResponse("Certification failed")
    
    print("Get submitResult from room %s" % (roomid))

    try:
        result = json.loads(request.body)
    except:
        return HttpResponse("Invalid json")
                 
    

def startRoom(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
        time = request.GET['time']
    except:
        return HttpResponse("Invalid request")

    if key != secretkey.secretKey:
        return HttpResponse("Certification failed")
         
    cmd = "python3 plug-ins/goldennum.py " + secretkey.secretKey + " " + request.GET['roomid'] + " " + request.GET['time']
    cmd_run = "nohup " + cmd + " >> log/" + request.GET['roomid'] + ".out&"

    try:
        room = Room.objects.get(roomid=request.GET['roomid'])
        if room.status == "on":
            return HttpResponse("Room alright started")
        else:
            room.status = "on"
            room.time = request.GET['time']
            room.cmd = cmd
            room.lastTime = str(int(time.time()))
            room.save()

            os.system(cmd_run)
            return HttpResponse("Room restarted")
    except:
        newRoom = Room()
        newRoom.status = "on"
        newRoom.roomid = request.GET['roomid']
        newRoom.time = request.GET['time']
        newRoom.history = json.dumps([])
        newRoom.cmd = cmd
        newRoom.lastTime = str(int(time.time()))
        newRoom.save()

        os.system(cmd_run)
        return HttpResponse("Room started new")
        
    # except:
    #     return HttpResponse("Invalid request")

def stopRoom(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        HttpResponse("Invalid request")

    if key != secretkey.secretKey:
        HttpResponse("Certification failed")
    
    try:
        room = Room.objects.get(roomid=roomid)
    except:
        return HttpResponse("No room match roomid")   

    cmd_kill = 'pkill -f "' + room.cmd + '"'
    os.system(cmd_kill)
    room.status = "off"
    room.save()
    return HttpResponse("Room stopped")

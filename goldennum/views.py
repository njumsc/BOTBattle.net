import json
# import random
import os
import time

# from django.shortcuts import render
from django.http import HttpResponse

import secretkey
# from . import datamaker

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
    except:
        return HttpResponse("Invalid request")

    if num1 > 100 or num1 < 0 or num2 > 100 or num2 < 0:
        return HttpResponse("Numbers overflow")

    users = User.objects.filter(name=name).filter(room=roomid)    
    if len(users) != 0:
        user = users[0]
    else:
        user = User()
        user.name = name
        user.room = roomid
        user.score = "0"
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
        "userNum": len(users),
        "users":[]
    }
    for user in users:
        nums = user.act.split()
        userInfo = {
            "userName": user.name,
            "userAct":[
                float(nums[0]),
                float(nums[1])                
            ]
        }
        retjson["users"].append(userInfo)

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

    room = Room.objects.get(roomid=roomid)
    room.history = json.dumps(json.loads(room.history).append(result['goldenNum']))
    room.time = str(result['roundTime'])
    room.lastTime = str(int(time.time()))
    room.save()

    for userInfo in result['users']:
        userName = userInfo['userName']
        user = User.objects.get(name=userName, roomid=roomid)
        user.score = str(int(user.score) + userInfo['userScore'])
        user.save()
    
    return HttpResponse("Submit success")

def startRoom(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
        timer = request.GET['time']
    except:
        return HttpResponse("Invalid request")

    if key != secretkey.secretKey:
        return HttpResponse("Certification failed")
         
    cmd = "python3 plug-ins/goldennum.py " + secretkey.secretKey + " " + roomid + " " + timer
    cmd_run = "nohup " + cmd + " >> log/" + roomid + ".out&"

    rooms = Room.objects.filter(roomid=roomid)
    if len(rooms) == 0:
        newRoom = Room()
        newRoom.status = "on"
        newRoom.roomid = roomid
        newRoom.time = timer
        newRoom.history = json.dumps([])
        newRoom.cmd = cmd
        newRoom.lastTime = str(int(time.time()))
        newRoom.save()
        os.system(cmd_run)
        return HttpResponse("Room started new")
    else:
        room = rooms[0]
        flag = os.system('ps axu | grep "' + room.cmd +'" | grep -v "grep" | wc -l')
        if flag == "0" or room.status != "on":
            room.status = "on"
            room.time = timer
            room.cmd = cmd
            room.lastTime = str(int(time.time()))
            room.save()
            os.system(cmd_run)
            return HttpResponse("Room restarted")
        else:
            return HttpResponse("Room started")

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

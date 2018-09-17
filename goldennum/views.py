import json
import random
import os
import time

from django.shortcuts import render
from django.http import HttpResponse

import secretkey
# from . import datamaker

from goldennum.models import User, Room
# Create your views here.

def index(request):
    return render(request, 'goldennum/goldennum.html')

def getStatus(request):
    retval = {
        "status": "success",
        "roomid": "",
        "history": [],
        "users": [],
        "time": 0
    }
    try:
        roomid = request.GET['roomid']
    except:
        retval['status'] = "Invalid request"
        return HttpResponse(json.dumps(retval))

    try:
        room = Room.objects.get(roomid=roomid)
    except:
        retval['status'] = "Room doesnot exist"
        return HttpResponse(json.dumps(retval))

    users = User.objects.filter(room=roomid)

    retval['roomid'] = roomid
    retval['history'] = json.loads(room.history)
    retval['time'] = int(room.time) - (int(time.time()) - int(room.lastTime))
    for user in users:
        retval['users'].append({
            "userName": user.name,
            "score": (user.score)
        })

    return HttpResponse(json.dumps(retval))

def userReg(request):
    # print(request.GET['name'])
    try:
        name = request.GET['name']
    except:
        return HttpResponse("Invalid request")

    if request.session.get("name") is None:
        users = User.objects.filter(name=name).filter(room="NULL")
        if users:
            user = users[0]
            if user.status == "on":
                return HttpResponse("User exist")
            else:
                request.session['name'] = name
                user.status = "on"
                user.save()
                return HttpResponse("User login success")
        else:
            newUser = User()
            newUser.name = name
            newUser.room = "NULL"
            newUser.score = "0"
            newUser.act = ""
            newUser.status = "on"
            newUser.save()
            request.session['name'] = name
            return HttpResponse("User register success")
    else:
        return HttpResponse("You have logged in")


def userOut(request):
    try:
        name = request.session['name']
    except:
        return HttpResponse("No login")

    user = User.objects.filter(name=name).filter(room="NULL")[0]
    user.status = "off"
    user.save()
    del request.session['name']
    print(user.status)
    return HttpResponse("Logout success")

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

    if num1 >= 100 or num1 <= 0 or num2 >= 100 or num2 <= 0:
        return HttpResponse("Numbers overflow")

    users = User.objects.filter(name=name).filter(room=roomid)
    if users:
        user = users[0]
    else:
        user = User()
        user.name = name
        user.room = roomid
        user.score = "0"
    user.act = str(num1) + " " + str(num2)
    user.save()

    return HttpResponse("Upload success")

def userStatus(request):
    try:
        name = request.session['name']
    except:
        return HttpResponse("No User Log In")
    return HttpResponse(name)

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
        user.act = str(random.random() * 100) + " " + str(random.random() * 100)
        user.save()

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
    # print(json.loads(room.history))
    room.history = json.dumps(json.loads(room.history) + [result['goldenNum']])
    # print(json.loads(room.history))
    room.time = str(result['roundTime'])
    room.lastTime = str(int(time.time()))
    room.save()

    for userInfo in result['users']:
        userName = userInfo['userName']
        user = User.objects.get(name=userName, room=roomid)
        user.score = str(int(user.score) + userInfo['userScore'])
        user.save()

    return HttpResponse("Submit success")

def roomStatus(request):
    try:
        roomid = request.GET['roomid']
    except:
        return HttpResponse("Invalid request")
         
    rooms = Room.objects.filter(roomid=roomid)
    if not rooms:
        return HttpResponse("The Room is off")
    else:
        return HttpResponse("on")    

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
    if not rooms:
        newRoom = Room()
        newRoom.status = "on"
        newRoom.roomid = roomid
        newRoom.time = timer
        newRoom.history = json.dumps([0])
        newRoom.cmd = cmd
        newRoom.lastTime = str(int(time.time()))
        newRoom.save()
        os.system(cmd_run)
        return HttpResponse("Room started new")
    else:
        room = rooms[0]
        # flag = os.system('ps axu | grep "' + room.cmd +'" | grep -v "grep" | wc -l')
        # print(json.dumps(flag))
        if room.status != "on":
            room.status = "on"
            room.time = timer
            room.cmd = cmd
            room.lastTime = str(int(time.time()))
            room.save()
            os.system(cmd_run)
            return HttpResponse("Room restarted")
        else:
            return HttpResponse("Room have started")

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

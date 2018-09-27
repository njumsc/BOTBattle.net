import json
import random
import os
import sys
import time

from django.shortcuts import render
from django.http import HttpResponse
from importlib import import_module

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
        "scores": {},
        "time": 0
    }
    try:
        roomid = request.GET['roomid']
    except:
        retval['status'] = "Invalid request"
        return HttpResponse(json.dumps(retval))

    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            retval['status'] = "Invalid roomid"
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
    if retval['time'] <= 0:
        retval['time'] = 10
        retval['status'] = "Game plug-in dump"
        retval['scores'] = { user.name: user.score for user in users}

    return HttpResponse(json.dumps(retval))

def userReg(request):
    # print(request.GET['name'])
    try:
        name = request.GET['name']
    except:
        return HttpResponse("Invalid request")

    for c in name:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponse("Invalid username")
    if len(name) > 10:
        return HttpResponse("Invalid username")

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
            newUser.useScript = str()
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

    for c in name:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponse("Invalid username")
    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponse("Invalid roomid")

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
        user.useScript = str()

    if user.useScript:
        return HttpResponse("User action has been consigned to script")

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

    try:
        room = Room.objects.get(roomid=roomid)
    except:
        return HttpResponse("Room doesnot exist")

    # retjson = datamaker.randomUsers()
    print("Get getAct from room %s" % (roomid))

    users = User.objects.filter(room=roomid)
    retjson = {
        "userNum": len(users),
        "users":[]
    }
    for user in users:
        if not user.useScript:
            nums = [float(n) for n in user.act.split()]
            user.act = "0 0"
            user.save()
        else:
            getNumbers = import_module(f'tmp.scripts.{roomid}.{user.name}').getNumbers
            nums = getNumbers(json.loads(room.history))
            if not (isinstance(nums, list) and len(nums) == 2):
                nums = [0.0, 0.0]

        # Update user act history of this room
        # print(json.loads(room.history))
        history = json.loads(room.history)
        if user.name not in history["userActs"]:
            history["userActs"][user.name] = []
        history["userActs"][user.name].append(nums)
        room.history = json.dumps(history)

        retjson["users"].append({
            "userName": user.name,
            "userAct": nums
        })
    room.save()
    print(retjson)
    return HttpResponse(json.dumps(retjson))

def userScript(request):
    try:
        name = request.session['name']
        roomid = request.GET['roomid']
    except:
        return HttpResponse("No login")

    users = User.objects.filter(name=name).filter(room=roomid)
    if users:
        user = users[0]
    else:
        user = User()
        user.name = name
        user.room = roomid
        user.score = "0"
        user.useScript = str()
    
    filename = f"./tmp/scripts/{user.room}/{user.name}.py"

    if request.method == "POST":
        with open(filename, "wb") as f:
            f.write(request.body)
        user.useScript = str(True)
        user.save()
        return HttpResponse("Script created successfully")
    elif request.method == "DELETE":
        if user.useScript:
            os.remove(filename)
            user.useScript = str()
            user.save()
        return HttpResponse("Script deleted")
    else:
        return HttpResponse("Invalid method")

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
        result = json.loads(request.body.decode('utf-8'))
    except:
        try:
            result = json.loads(request.body)
        except:
            return HttpResponse("Invalid json")

    room = Room.objects.get(roomid=roomid)

    # Update golden number history of this room
    if result['goldenNum'] != 0:
        history = json.loads(room.history)
        history['goldenNums'].append(result['goldenNum'])
        room.history = json.dumps(history)
    # print(json.loads(room.history))

    room.time = str(result['roundTime'])
    room.lastTime = str(int(time.time()))
    room.save()

    for userInfo in result['users']:
        userName = userInfo['userName']
        user = User.objects.get(name=userName, room=roomid)
        user.score = str(int(user.score) + userInfo['userScore'])
        user.save()

    print(result)

    return HttpResponse("Submit success")

def roomStatus(request):
    try:
        roomid = request.GET['roomid']
    except:
        return HttpResponse("Invalid request")

    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponse("Invalid username")
         
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

    cmd = f'python3 plug-ins/goldennum.py "{secretkey.secretKey}" {roomid} {timer}'
    cmd_run = f'nohup {cmd} >> tmp/logs/{roomid}.out'

    if sys.platform == "win32":
        cmd_run = f'start /b {cmd_run}'
    else:
        cmd_run = f'{cmd_run} &'
        
    rooms = Room.objects.filter(roomid=roomid)
    if not rooms:
        newRoom = Room()
        newRoom.status = "on"
        newRoom.roomid = roomid
        newRoom.time = timer
        newRoom.cmd = cmd.replace('"', '')
        newRoom.lastTime = str(int(time.time()))
        newRoom.history = json.dumps({
            "goldenNums": [],
            "userActs": {}
        })
        newRoom.save()
        os.makedirs("./tmp/logs", exist_ok=True)
        os.system(cmd_run)
        return HttpResponse("Room started new")
    else:
        room = rooms[0]
        # flag = os.system('ps axu | grep "' + room.cmd +'" | grep -v "grep" | wc -l')
        # print(json.dumps(flag))
        if room.status != "on":
            room.status = "on"
            room.time = timer
            room.cmd = cmd.replace('"', '')
            room.lastTime = str(int(time.time()))
            room.save()
            os.makedirs("./tmp/logs", exist_ok=True)
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

    if sys.platform == "win32":
        room_cmd = room.cmd[len("python3 "):] # skip 'python3 ' prefix
        cmd_kill = f'wmic process where "COMMANDLINE LIKE \'%{room_cmd}%\'" call terminate'
    else: 
        cmd_kill = f'pkill -f "{room.cmd}"'
    os.system(cmd_kill)
    room.status = "off"
    room.save()
    return HttpResponse("Room stopped")

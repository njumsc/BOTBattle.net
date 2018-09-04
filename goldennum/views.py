import json
import random
import os

from django.shortcuts import render
from django.http import HttpResponse

import secretkey
from . import datamaker
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
            cmd = "python3 plug-ins/goldennum.py " + secretkey.secretKey + " " + request.GET['roomid'] + " " + request.GET['time']
            cmd_run = "nohup " + cmd + " &"
            cmd_kill = "kill -s 9"
            os.system(cmd_run)
            return HttpResponse("success")
        else:
            HttpResponse("Certification failed")
    except:
        return HttpResponse("Invalid request")
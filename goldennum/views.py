import json

from django.shortcuts import render
from django.http import HttpResponse

import secretkey

# Create your views here.

def getAct(request):
    sampjson = {
        "userNum": 3,
        "users": [
            {
                "userName": "user1",
                "userAct": [
                    1.1,
                    8.9
                ]
            },
            {
                "userName": "user2",
                "userAct": [
                    3.2,
                    7.4
                ]
            },
            {
                "userName": "user3",
                "userAct": [
                    23.5,
                    92.1
                ]
            }
        ]
    }
    try:
        if request.GET['key'] == secretkey.secretKey:
            print("Get getAct from room %s" % (request.GET['roomid']))
            return HttpResponse(json.dumps(sampjson))
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
    return HttpResponse("1")
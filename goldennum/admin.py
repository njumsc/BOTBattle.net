from django.contrib import admin
from .models import Room, User
import secretkey
import json
import time
import sys
import os

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    fields = ['roomid', 'time', 'status']

    def save_model(self, request, obj, form, change):
        roomid = request.POST['roomid']
        timer = request.POST['time']

        cmd = f'python3 goldennum/RoomThread.py "{secretkey.secretKey}" {roomid} {timer}'
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
        else:
            room = rooms[0]
            if room.status != "on":
                room.status = "on"
                room.time = timer
                room.cmd = cmd.replace('"', '')
                room.lastTime = str(int(time.time()))
                room.save()
                os.makedirs("./tmp/logs", exist_ok=True)
                os.system(cmd_run)


class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'room', 'score', 'status']


# when debugging, show all fields
# admin.site.register(Room)
# admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)

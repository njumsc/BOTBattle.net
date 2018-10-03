from django.contrib import admin
from .models import Room, User

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    fields = ['roomid', 'time']


class UserAdmin(admin.ModelAdmin):
    fields = ['name', 'room', 'score', 'status']


# when debugging, show all fields
# admin.site.register(Room)
# admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from . models import Message, Room, Task, Topic, Result

# Register your models here.
admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Result)

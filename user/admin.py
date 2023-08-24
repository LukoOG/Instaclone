from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(DMGroup)
admin.site.register(DMMessage)
admin.site.register(DMManager)
#admin.site.register(save)
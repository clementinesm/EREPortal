from django.contrib import admin
import importlib
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'get_username', 'access_level', 'note')


    def get_username(self, obj):
        return obj.user.username

admin.site.register(UserProfile, UserProfileAdmin)


class GraphNamesAdmin(admin.ModelAdmin):
    model = GraphNames
    list_display = ('id', 'url_name', 'long_name', 'required_access_level', 'active', 'note')

    def get_username(self, obj):
        return obj.user.long_name

admin.site.register(GraphNames, GraphNamesAdmin)



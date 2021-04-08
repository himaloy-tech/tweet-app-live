from django.contrib import admin
from django.contrib.auth import models
from .models import User, Post, Follower, Following
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "datetime")

class FollowingAdmin(admin.ModelAdmin):
    filter_horizontal = ("user_following", )
class FollowerAdmin(admin.ModelAdmin):
    filter_horizontal = ("user_following", )
admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Following, FollowingAdmin)
from django.contrib import admin

# Register your models here.

from user_action.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Post, Comment


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = False
    fields = ['text', 'author', 'publication_date']
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'body', 'image', 'author', 'publication_date']
    inlines = (CommentInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
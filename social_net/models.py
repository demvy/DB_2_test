#! -*-coding:utf-8 -*-
from django.db import models
from user_action.models import Profile

# Create your models here.

from datetime import datetime as dt


class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    body = models.TextField(max_length=3000, null=True, blank=False)
    image = models.ImageField(null=True, blank=False, upload_to='images/')
    author = models.ForeignKey(Profile)
    likes = models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    publication_date = models.DateTimeField(default=dt.now())

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return "{} by {}".format(self.title, self.author.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True)
    author = models.ForeignKey(Profile, null=True)
    text = models.TextField(max_length=500, null=True, blank=False)
    publication_date = models.DateTimeField(default=dt.now())

    def __str__(self):
        if self.text is not None:
            return "{} by {} to {}".format(self.text[:20], self.author.user.username, self.post.title)
        else:
            return self.post.title

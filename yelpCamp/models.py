from django.db import models
from django.contrib.auth.models import User


class Campground(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    imageUrl = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.name


class Comment(models.Model):
    campground = models.ForeignKey(Campground, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField('comment timestamp')

    def __str__(self):
        return self.text


from django.db import models

# Create your models here.
class Campground(models.Model):
    name = models.CharField(max_length=100)
    imageUrl = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


default_image_path = 'images/default.jpg'


class Event(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now)
    desc = models.CharField(max_length=4000, null=True)
    imageUrl = models.ImageField(
        upload_to='static/images/im',
        verbose_name='Картинка',
        default=default_image_path,
        max_length=256,
        null=False)
    participation = models.ManyToManyField(User)

    def __str__(self):
        return "Id=%d, Name=%s, time=%s, address=%s"\
            % (self.id, self.name, self.time, self.address)

class EventPrevious(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now)
    desc = models.CharField(max_length=4000, null=True)
    imageUrl = models.ImageField(
        upload_to='static/images/im',
        verbose_name='Картинка',
        default=default_image_path,
        max_length=256,
        null=False)
    participation = models.ManyToManyField(User)

    def __str__(self):
        return "Id=%d, Name=%s, time=%s, address=%s"\
            % (self.id, self.name, self.time, self.address)
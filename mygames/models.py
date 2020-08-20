
from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
User = get_user_model()


class LoggedUser(models.Model):
    username = models.CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.username


class Games(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image_path = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite = models.OneToOneField(
        Games, related_name='customuser', on_delete=models.CASCADE, default=1)

    def __str__(self):
        print("Hapahapa ", self.player.username)
        return self.player.username


class GamesPlayed(models.Model):
    player = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    game = models.OneToOneField(
        Games, on_delete=models.CASCADE, blank=True, default=1)


class Friend(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ManyToManyField(User)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, max_length=20,
                             on_delete=models.CASCADE, null=True)
    title = models.CharField(blank=True, null=True, max_length=200)
    description = models.CharField(blank=True, null=True, max_length=200)
    playerno = models.CharField(max_length=20, null=True)
    published_date = models.DateTimeField(
        blank=True, default=timezone.now, max_length=200)
    request_duration = models.CharField(max_length=40, null=True)
    requestStatus = models.BooleanField()
    messageStatus = models.BooleanField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Message(models.Model):
    contact = models.ForeignKey(
        CustomUser, related_name='messages', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    email = models.CharField(blank=True, null=True, max_length=200)
    timestamp = models.DateTimeField(
        blank=True, default=timezone.now, max_length=200)

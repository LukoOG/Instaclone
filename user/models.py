from django.db import models
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

today = datetime.date.today()


#hello intruder, what is your purpose
# Create your models here.
def user_directory_path(instance, filename):
    return 'account/images/{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
                                     related_name='followed_by',
                                     symmetrical=False,
                                     blank=True)

    profile_pic = models.ImageField(default='account/default.jpg',
                                    upload_to=user_directory_path,
                                    blank=True,
                                    null=True)

    def __str__(self):
        return self.user.username


class Reply(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='profile_reply',
                                on_delete=models.CASCADE)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)


def media_directory_path(instance, filename):
    return 'posts/media/{2}/{0}/{1}'.format(instance.profile.user.username,
                                            filename, today)


class Post(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='profile_post',
                                on_delete=models.CASCADE)
    media = models.FileField(upload_to=media_directory_path,
                             null=True,
                             blank=True)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile)

    # def __str__(self):
    #     if self.message is None:
    #         return f'{self.profile.user.username} \n {self.date}'
    #     else:
    #         return f'{self.profile.user.username} \n {self.message[:5]}  \n {self.date}'


class Comment(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='profile_comment',
                                on_delete=models.CASCADE)
    edited = models.BooleanField(blank=True, null=True, default=False)
    post = models.ForeignKey(Post,
                             related_name='post_comment',
                             on_delete=models.CASCADE)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} \n {self.date}'

    #     else:
    #     return f'{self.profile.user.username}{self.message[:5]} {self.date}'


#The model calsses for the dms
from django.db import models
from django.core.exceptions import ValidationError


class DMGroup(models.Model):
    participants = models.ManyToManyField(Profile,
                                          symmetrical=False,
                                          through='DMManager')
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return f'{self.id}'

class DMMessage(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    edited = models.BooleanField(blank=True, null=True, default=False)
    DM = models.ForeignKey(DMGroup,
                           on_delete=models.CASCADE,
                           related_name='messages')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        other_participant = self.DM.participants.exclude(id=self.sender.id).first()
        return f"{self.sender}: [{self.message[:255]}] in {other_participant}'s dm"


class DMManager(models.Model):
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    DM = models.ForeignKey(DMGroup, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['participant', 'DM'],
                                    name='unique_participants_dm')
        ]

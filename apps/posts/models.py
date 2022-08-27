from django.db import models
from users.models import UserProfile
from apps.projects.models import Project
from Minimo import settings
from apps.social.models import Follow

class Memo(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='memo', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='memo', on_delete=models.CASCADE)
    contents = models.TextField(verbose_name='Memo')
    image = models.FileField(upload_to='media', null=True)
    number = models.IntegerField(verbose_name='Title Number')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='comment', on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)


class Clap(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='clap', on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, related_name='clap', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, related_name='clap', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Readable(models.Model) :
    target = models.ForeignKey(UserProfile, related_name='readable', on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, related_name='letread', on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, related_name='whocanread', on_delete=models.CASCADE)
    muted = models.IntegerField(verbose_name='Muted', default=0)


class Alert(models.Model):
    user = models.ForeignKey(UserProfile, related_name='alert', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='alert', on_delete=models.CASCADE, blank=True, null=True)
    clap = models.ForeignKey(Clap, related_name='alert', on_delete=models.CASCADE, blank=True, null=True)
    follow = models.ForeignKey(Follow, related_name='alert', on_delete=models.CASCADE, blank=True, null=True)
    read = models.IntegerField(verbose_name='Read', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
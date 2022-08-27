from django.db import models
from users.models import UserProfile
from apps.social.models import Group


class Project(models.Model):
    user = models.ForeignKey(UserProfile, related_name='projects', on_delete=models.CASCADE)
    pname = models.CharField(verbose_name='Project name', max_length=255)
    group = models.ForeignKey(Group, related_name='canread', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscribe(models.Model):
    target = models.ForeignKey(Project, related_name='subscriber', on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, related_name='subscribed', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
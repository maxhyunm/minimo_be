from django.db import models
from users.models import UserProfile


class Group(models.Model) :
    user = models.ForeignKey(UserProfile, related_name='groups', on_delete=models.CASCADE)
    gname = models.CharField(verbose_name='Group name', max_length=50)
    # member = models.JSONField(verbose_name='Members', null=True)
    # member = models.ListField(models.ForeignKey('MinimoUser'))
    # def add_obj(self, obj):
    #     self.list.append(obj)
    #     self.save()
    # def remove_obj(self, obj):
    #     self.list.remove(obj)
    #     self.save()


class Grouping(models.Model) :
    target = models.ForeignKey(UserProfile, related_name='groupedby', on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, related_name='grouping', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class Follow(models.Model):
    target = models.ForeignKey(UserProfile, related_name='follower', on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class Mute(models.Model):
    target = models.ForeignKey(UserProfile, related_name='mutedby', on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, related_name='muted', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


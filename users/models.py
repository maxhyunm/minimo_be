from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class MinimoUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        super(MinimoUser, self).save(**kwargs)
        check = UserProfile.objects.filter(user=self)
        if len(check) == 0 :
            name = str(self.email).split('@')[0]
            prof = UserProfile(user=self, username=name)
            prof.save()


class UserProfile(models.Model):
    user = models.ForeignKey(MinimoUser, related_name='profile', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='NickName', max_length=50)
    picture = models.FileField(verbose_name='Profile Picture', upload_to='media', null=True, blank=True)
    describe = models.CharField(verbose_name='Describe', max_length=500, null=True, blank=True)
    # following = models.ManyToManyField("self", related_name="follower", blank=True, symmetrical=False)
    # mutes = models.ManyToManyField("self", related_name="muted", blank=True, symmetrical=False)
    # subscribes = models.ManyToManyField("Projects", related_name="subscriber", blank=True, symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)






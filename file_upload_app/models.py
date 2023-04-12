from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class File(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads',null=True)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='files')

    def __str__(self):
        return self.title

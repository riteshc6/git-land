from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Ssh_key(models.Model):
    key_name = models.CharField(max_length=50)
    ssh_key = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='ssh_keys')


class Repository(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='repositories')
    repo_path = models.FilePathField()
    create_time = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField()


class Test_info(models.Model):
    commit_id = models.CharField(max_length=100)
    commit_message = models.TextField()
    repo = models.ForeignKey(
        'Repository', on_delete=models.CASCADE, related_name='tests',null=True)
    test_exit_code = models.IntegerField()
    log = models.TextField()

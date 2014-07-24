#coding: utf-8
from django.db import models

class DeployLogs(models.Model):
    project = models.CharField(max_length = 30,)
    reason = models.CharField(max_length = 30,)
    excutor = models.CharField(max_length = 10)
    do_date = models.DateTimeField()
    
class projects(models.Model):
    name = models.CharField(max_length = 30)
    repo = models.CharField(max_length = 30)
    source_dir = models.CharField(max_length = 30)
    target_dir = models.CharField(max_length = 30)
    hosts = models.CharField(max_length = 300)
    status = models.IntegerField(max_length = 1, help_text = '0:enable, 1:disable')
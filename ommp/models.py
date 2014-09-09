#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

class IDCs(models.Model):
    '''
    Internet Data Center informations, store
    '''
    idc_name = models.CharField(max_length = 20)
    address = models.CharField(max_length = 50)
    display_addr = models.CharField(max_length = 20)
    contact = models.CharField(max_length = 4)
    phone_num = models.CharField(max_length = 12)
    email = models.EmailField(max_length = 50)
    code = models.IntegerField(max_length = 6)
    add_time = models.DateTimeField()
    end_date = models.CharField(max_length = 10)
    
class Cabinets(models.Model):
    name = models.CharField(max_length = 30)
    idc = models.ForeignKey(IDCs)
    admin = models.ForeignKey(User)
    size = models.CharField(max_length = 30)
    add_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    servers = models.IntegerField(max_length = 2)
    available = models.IntegerField(max_length = 1)
    
class Projects(models.Model):
    '''
    projects informations
    '''
    name = models.CharField(max_length = 30)
    repo = models.CharField(max_length = 30)
    source_dir = models.CharField(max_length = 30)
    target_dir = models.CharField(max_length = 30)
    status = models.IntegerField(max_length = 1, help_text = '0:enable, 1:disable')

class IPs(models.Model):
    ip = models.IPAddressField(max_length = 15)
    idc = models.ForeignKey(IDCs)
    is_used = models.IntegerField(max_length = 1)

class Servers(models.Model):
    name = models.CharField(max_length = 30)
    idc = models.ForeignKey(IDCs)
    cabinets = models.ForeignKey(Cabinets, related_name='cab_name')
    os = models.CharField(max_length = 30)
    size = models.CharField(max_length = 10)
    parts = models.CharField(max_length = 30)
    add_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    father = models.ForeignKey('self', null = True)
    used_type = models.IntegerField(max_length = 1)
    admin = models.ForeignKey(User)

class Relations(models.Model):
    ip = models.ForeignKey(IPs)
    project = models.ForeignKey(Projects)

class DeployLogs(models.Model):
    '''
    store deploy logs
    '''
    project = models.CharField(max_length = 30,)
    reason = models.CharField(max_length = 30,)
    excutor = models.CharField(max_length = 10)
    do_date = models.DateTimeField()
    
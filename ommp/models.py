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
    cellphone_num = models.CharField(max_length = 12, null = True)
    phone_num = models.CharField(max_length = 12, null = True)
    email = models.EmailField(max_length = 50)
    code = models.IntegerField(max_length = 6)
    add_time = models.DateTimeField()
    end_date = models.CharField(max_length = 10, null = True)
    
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
    name = models.CharField(max_length = 20)
    desc = models.CharField(max_length = 30)
    admin = models.CharField(max_length = 20)
    add_date = models.CharField(max_length = 10)
    repo = models.CharField(max_length = 100)
    language = models.CharField(max_length = 20)
    environment = models.CharField(max_length = 100)
    comment = models.CharField(max_length = 100, null = True)
    

class Servers(models.Model):
    name = models.CharField(max_length = 30)
    idc = models.ForeignKey(IDCs)
    cabinets = models.ForeignKey(Cabinets, related_name='cab_name', null = True)
    os = models.CharField(max_length = 30)
    size = models.CharField(max_length = 10)
    parts = models.CharField(max_length = 30)
    hostname = models.CharField(max_length = 120)
    login_name = models.CharField(max_length = 120)
    add_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    father = models.ForeignKey('self', null = True)
    used_type = models.IntegerField(max_length = 1)             #0:testing 1:product 2:disabled 3:available
    admin = models.ForeignKey(User)
    
class IPs(models.Model):
    ip = models.IPAddressField(max_length = 15)
    netmask = models.IPAddressField(max_length = 15)
    ip_type = models.IntegerField(max_length = 1)                   #0:private ip, 1:public ip
    idc = models.ForeignKey(IDCs)
    project = models.ForeignKey(Projects, null = True)
    status = models.IntegerField(max_length = 1, null = True)       #0:enable, 1:disable, 2:is_used
    servers = models.ForeignKey(Servers, null = True)
    used_for = models.IntegerField(max_length = 1, null = True)      #0:real_ip, 1:VIP, 2:manage_ip
    comment = models.CharField(max_length = 50)

class Relations(models.Model):
    public_ip = models.ForeignKey(IPs, null = True, related_name='public_ip')
    public_port = models.IntegerField(max_length = 5, null = True)
    private_ip = models.ForeignKey(IPs, null = True, related_name='puivate_ip')
    private_port = models.IntegerField(max_length = 5, null = True)
    pro_ip = models.ForeignKey(IPs, null = True, related_name = 'pro_ip')
    project = models.ForeignKey(Projects, null = True)
    relation_type = models.IntegerField(max_length = 1)             #0:ip relation, 1:ip-project relation
    comment = models.CharField(max_length = 50, null = True)
    check_code = models.CharField(max_length = 32, null = True)
    
class Templates(models.Model):
    name = models.CharField(max_length = 50)
    project = models.ForeignKey(Projects)
    target_type = models.IntegerField(max_length = 1)                   #1: as project, 2: as hosts
    hosts = models.CharField(max_length = 9999, null = True)
    threads = models.IntegerField(max_length = 2)
    is_backup = models.IntegerField(max_length = 1)                     #0: false    1:true
    backup_dir = models.CharField(max_length = 120, null = True)
    login_user = models.CharField(max_length = 30, null = True)
    addition_args = models.CharField(max_length = 120)
    source_dir = models.CharField(max_length = 150)
    temporary_dir = models.CharField(max_length = 150, null = True)
    target_dir = models.CharField(max_length = 150)
    exclude_files = models.TextField(null = True)
    after_operations = models.CharField(max_length = 2000, null = True)
    
class Task_logs(models.Model):
    task_log_id = models.CharField(db_index = True, max_length = 20)
    job_id = models.CharField(db_index = True, max_length = 36)
    template = models.ForeignKey(Templates)
    config = models.TextField()
    add_time = models.DateTimeField()
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    oper_user = models.ForeignKey(User)
    status_code = models.IntegerField(max_length = 1, db_index = True)                       #0:pending, 1:doing, 2:pause, 3:terminated, 4:done, 5: cancel
    status = models.TextField(null = True)
    back_file = models.CharField(max_length = 120, null = True)
    back_file_code = models.CharField(max_length = 32, null = True)
    
#    pro_status = models.

class DeployLogs(models.Model):
    '''
    store deploy logs
    '''
    project = models.CharField(max_length = 30,)
    reason = models.CharField(max_length = 30,)
    excutor = models.CharField(max_length = 10)
    do_date = models.DateTimeField()
    
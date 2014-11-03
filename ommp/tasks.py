#coding: utf-8
from __future__ import absolute_import
from ommp.celery import app
import threading
from ommp.resources.base import local, get_datetime
import os
import datetime
from hashlib import md5
from ommp.models import Task_logs

class DeployThreads(threading.Thread):
    '''mut-thread hand deploy'''
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.kwargs = kwargs
        
        
    def run(self):
        hosts = self.kwargs['hosts']
        target_dir = os.path.abspath(self.kwargs['target_dir'])
        source_dir = os.path.abspath(self.kwargs['source_dir'])
        exclude_files = self.kwargs['exclude_files']
        after_operations = self.kwargs['after_operations']
        temporary_dir = os.path.abspath(self.kwargs['temporary_dir'])
        addition_args = self.kwargs['addition_args']
        task = self.kwargs['task_id']
        
        
        command = 'rsync -azx '
        if addition_args:
            command += str(addition_args)
            
        if exclude_files:
            exclude_file_list =[os.path.join(source_dir, x) for x in exclude_files.split('\n')]
            exclude = ' --exclude ' + ' --exclude '.join(exclude_file_list)
            command += str(exclude)
            
        for h in hosts:
            command += ' %s/ %s:%s' % (source_dir, h, target_dir)
            out, err = local(command)
            if err:
                status = '%s:%s' % (h, err)
            else:
                status = '%s:Done' % (h)
                
            if mutex.acquire(1):
                try:
                    _sync_status_detail_db(task, status = status)
                except:
                    pass
                finally:
                    mutex.release()
        
        
        
#        if temporary_dir:
#            target_dir = temporary_dir
            
                
    
mutex = threading.Lock()
    
def _sync_status_detail_db(task_id, **kwargs):
    if task_id:    
        task_log = Task_logs.objects.get(id = task_id)
        
    if kwargs:
        keys = kwargs.keys()
        for k in keys:
            if k == 'status':
                detail = '' if not task_log.status else task_log.status
                detail += kwargs[k]
                task_log.status = detail + '\n'
            elif k == 'end_time':
                task_log.end_time = kwargs[k]
            elif k == 'status_code':
                task_log.status_code = kwargs[k]
            elif k == 'back_file':
                task_log.back_file = kwargs[k]
            elif k == 'back_file_code':
                task_log.back_file_code = kwargs[k]
            elif k == 'start_time':
                task_log.start_time = kwargs[k]
            elif k == 'end_time':
                task_log.end_time = kwargs[k]
        
        return True if task_log.save() == None else False
        

def get_file_validate_code(name):
    m = md5()
    with open(name, 'rb') as a_file:
        m.update(a_file.read())
    return m.hexdigest()

def _do_backup(project, source_dir, backup_dir):
    back_file_name = project
    back_file_suffix = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    
    if backup_dir:
        if not os.path.isdir(backup_dir):
            try:
                os.makedirs(backup_dir)
            except:
                pass
        back_file = '%s.tgz' %(os.path.abspath(os.path.join(backup_dir, back_file_name + '_' + back_file_suffix)))
    else:
        back_file = '%s.tgz' %(os.path.abspath(os.path.join(os.path.abspath(os.path.join(source_dir, '..')), back_file_name + '_' + back_file_suffix)))
        
    
    source_father = os.path.abspath(os.path.join(source_dir, '..'))
    t = source_dir.split('/')
    source_file_name = t[-1] if t[-1] else t[-2]
    command = 'cd %s;tar -zcf %s %s' % (source_father, back_file, source_file_name)
    out, err = local(command)
    return out, err, back_file


def split_hosts_to_threads(threads, hosts):
    '''assagin hosts to every thread'''
    host_count = len(hosts)
    threads = host_count if threads > host_count else threads
    host_count_per_thread = host_count / threads
    
    host_list_per_thread = []
    
    for i in range(0, threads):
        host_list_per_thread.append(hosts[0:host_count_per_thread])
        del hosts[0:host_count_per_thread]
        
    for i in range(0, len(hosts)):
        host_list_per_thread[i].append(hosts[i])
        
    return host_list_per_thread


@app.task
def start_deploy(config):
    project = config['project']
    source_dir = config['source_dir']
    backup_dir = config['backup_dir']
    task = config['task_id']
    target_dir = config['target_dir']
    exclude_files = config['exclude_files']
    after_operations = config['after_operations']
    temporary_dir = config['temporary_dir']
    addition_args = config['addition_args']

    start_time = get_datetime()
    _sync_status_detail_db(task, start_time = start_time)
    
    if config['is_backup'] == '1':
        
        #backup the source and store statue
        out, err, file = _do_backup(project, source_dir, backup_dir)
        if not err:
            file_code = get_file_validate_code(file)
            _sync_status_detail_db(task, 
                                   status_code = '1',
                                   back_file = file,
                                   back_file_code = file_code,
                                   status = 'backup:success\nbackup_file:%s' % file
                                   )
        else:
            _sync_status_detail_db(task, 
                                   status = 'backup failed!'
                                   )
    else:
        pass
    
    #assagin hosts to every thread
    threads = int(config['threads'])
    hosts = config['do_hosts']
    host_list_per_thread = split_hosts_to_threads(threads, hosts)
    
    h_length = len(host_list_per_thread)
    
    
    for i in range(0, h_length):
        deploy_thread = DeployThreads(
                                      task_id = task,
                                      addition_args = addition_args,
                                      source_dir = source_dir,
                                      hosts = host_list_per_thread[i], 
                                       target_dir = target_dir,
                                       exclude_files = exclude_files,
                                       after_operations = after_operations,
                                       temporary_dir = temporary_dir,
                                       )
        deploy_thread.start()
        
        if i == h_length - 1:
            deploy_thread.join()
        
    end_time = get_datetime()
    _sync_status_detail_db(task, end_time = end_time, status_code = 4)























    
#coding: utf-8
from __future__ import absolute_import
from ommp.celery import app
import threading
from ommp.resources.base import local, get_datetime
import os
import datetime, time
from hashlib import md5
from ommp.models import Task_logs
import salt.client as client

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
        temporary_dir = self.kwargs['temporary_dir']
        addition_args = self.kwargs['addition_args']
        task = self.kwargs['task_id']
        
        local_command = ';'.join(after_operations.strip().split('\r\n'))
        
        command = 'cd %s;rsync -azx ' % source_dir
        if addition_args:
            command += addition_args
            
        if exclude_files:
            exclude_file_list = [x for x in exclude_files.split('\r\n') if x]
            exclude = ' --exclude ' + ' --exclude '.join(exclude_file_list)
            command += exclude
            
        for h in hosts:
            
            th = h[0]
            host_name = h[1]
            
            if temporary_dir:
                tdir = os.path.abspath(temporary_dir)
                command += ' ./ %s:%s' % (th, tdir)
                out, err = local(command)
                
                com = 'cd %s;rsync -azx %s %s ./ %s;' % (tdir, addition_args, exclude, target_dir)
                com += local_command
                exc_command_re = _exec_remote_command(host_name, com)['stderr']
            else:
                command += ' ./ %s:%s' % (th, target_dir)
                out, err = local(command)
                exc_command_re = _exec_remote_command(host_name, local_command)['stderr']

            if err or exc_command_re:
                status = '\n%s:%s\n%s' % (th, err, exc_command_re)
            else:
                status = '\n%s:Done' % (th)
                
            if mutex.acquire(1):
                try:
                    _sync_status_detail_db(task, status = status)
                except:
                    pass
                finally:
                    mutex.release()
        

                
    
mutex = threading.Lock()


def _exec_remote_command(host_name, command):
        cl = client.LocalClient()
        re = cl.cmd(host_name,'cmd.run_all',[command],expr_form='list')
        return re[host_name]

    
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
    source_base_name = os.path.basename(os.path.abspath(source_dir))
    command = 'cd %s;tar -zcf %s %s' % (source_father, back_file, source_base_name)
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
    _sync_status_detail_db(task, 
                           start_time = start_time,
                           status_code = '1',
                           )
    
    if config['is_backup'] == '1':
        
        #backup the source and store statue
        out, err, file = _do_backup(project, source_dir, backup_dir)
        if not err:
            file_code = get_file_validate_code(file)
            _sync_status_detail_db(task, 
                                   back_file = file,
                                   back_file_code = file_code,
                                   status = 'backup:success\nbackup_file:%s' % file
                                   )
        else:
            _sync_status_detail_db(task, 
                                   status = 'backup: Failed \n backup_detail: %s' %(err)
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

    while threading.activeCount() >1:
        time.sleep(1)
    end_time = get_datetime()
    _sync_status_detail_db(task, status = 'task: All Done', end_time = end_time, status_code = 4)























    
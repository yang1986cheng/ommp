#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import json
import ommp.resources.base as base
from ommp.models import Projects, Relations, IPs, Templates, Task_logs
import salt.client as client
from ommp.celery import app

from django.core.signals import request_finished
import time

from ommp.tasks import start_deploy


def tasks(request):
    return render_to_response('tasks.html', context_instance=RequestContext(request))

def in_process(request):
    return render_to_response('task-in-process.html', context_instance=RequestContext(request))

def task_logs(request):
    return render_to_response('deploy-logs.html', context_instance=RequestContext(request))

@login_required
@csrf_protect
def add_task(request):
    po = request.REQUEST
    template_name = po.get('template-name','')
    target_project = po.get('target-project','')
    thread_count = po.get('thread-count', '')
    addition_args = po.get('add-args', '')
    exclude_files = po.get('exclude-files', '')
    login_name = po.get('login-name', '')
    source_dir = po.get('source-dir', '')
    target_dir = po.get('target-dir', '')
    is_save_backup = po.get('is-save-backup', '')
    task_as_host = po.get('task-as-host', '')
    temporary_dir = po.get('temporary-dir', '')
    after_operation = po.get('after-operation','')
    backup_dir = po.get('backup-dir', '')
    h = po.getlist('task-host')
    hosts = []
    
    for x in h:
        hosts.append(str(x))
    
    
    if not base.check_post_val(thread_count, template_name, target_project, source_dir, target_dir, ):
        raise Http404
    
    backup_dir = backup_dir if is_save_backup else ''
    
    task = Templates(name = template_name,
                     project = Projects.objects.get(id = target_project),
                     target_type = '2' if task_as_host else '1',
                     hosts = ','.join(hosts),
                     threads = thread_count,
                     is_backup = '0' if not is_save_backup else '1',
                     backup_dir = backup_dir,
                     login_user = login_name,
                     addition_args = addition_args,
                     source_dir = source_dir,
                     temporary_dir = temporary_dir,
                     target_dir = target_dir,
                     exclude_files = exclude_files,
                     after_operations = after_operation,
                 )
    
    raw_json = {'status' : 'success'} if task.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
    
@login_required
@csrf_protect
def update_task(request):
    po = request.REQUEST
    task_id = po.get('task-id', '')
    thread_count = po.get('thread-count', '')
    after_operation = po.get('after-operation','')
    addition_args = po.get('add-args', '')
    exclude_files = po.get('exclude-files', '')
    login_name = po.get('login-name', '')
    source_dir = po.get('source-dir', '')
    target_dir = po.get('target-dir', '')
    is_save_backup = po.get('is-save-backup', '')
    backup_dir = po.get('backup-dir', '')
    deploy_type = po.get('deploy-type', '')
    temporary_dir = po.get('temporary-dir', '')
    h = po.getlist('task-host')
    hosts = []
    
    for x in h:
        hosts.append(str(x))
    hosts = ','.join(hosts)
    
    if not base.check_post_val(thread_count, source_dir, task_id, target_dir, deploy_type):
        raise Http404
    
    backup_dir = backup_dir if is_save_backup else ''

    template = Templates.objects.get(id = task_id)
    if hosts:
        template.hosts = hosts
    else:
        pass
    template.target_type = deploy_type
    template.threads = thread_count
    template.is_backup = '1' if is_save_backup else '0'
    template.backup_dir = backup_dir
    template.login_user = login_name
    template.addition_args = addition_args
    template.source_dir = source_dir
    template.temporary_dir = temporary_dir
    template.target_dir = target_dir
    template.exclude_files = exclude_files
    template.after_operations = after_operation
    
    raw_json = {'status' : 'success'} if template.save() == None else {'status' : 'failed'}
    
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@login_required
@csrf_protect
def delete_task(request):
    po = request.REQUEST
    task_id = po.get('task-id', '')

    task = Templates.objects.get(id = task_id)
    
    raw_json = {'status' : 'success'} if task.delete() == None else {'status' : 'failed'}
    
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

    
@login_required
@csrf_protect
def list_templates(request):
    po = request.REQUEST
    list_type = po.get('list-type', '')
    page = po.get('page', '')
    rows = po.get('rows', '')
    template_list = []
#    return HttpResponse("bbbb")
    
    if list_type and int(list_type) == 1 and page and rows:
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        templates = Templates.objects.all()[r_from:r_end]
        total = Templates.objects.all().count()

        for template in templates:
            r = {'temp-id' : template.id,
                 'temp-name' : template.name,
                 'task-target' : template.project.name,
                 'target-type' : template.target_type,
                 'pro-id' : template.project.id,
                 'is-backup' : template.is_backup,
                 'login-user' : template.login_user,
                 'add-args' : template.addition_args,
                 'source-dir' : template.source_dir,
                 'temporary-dir' : template.temporary_dir,
                 'target-dir' : template.target_dir,
                 'exclude-files' : template.exclude_files,
                 'after-task' : template.after_operations,
                 'thread-count' : template.threads,
                 'backup-dir' : template.backup_dir,
                 }
            template_list.append(r)
            
        raw_json = {'total' : total, "rows" : template_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")

    
    else:
        return HttpResponse("xxx")

@login_required
@csrf_protect    
def add_task_to_list(request):
        task = request.REQUEST.get('task-id','')
        status_code = 0
        add_time = base.get_datetime()
        oper_user = request.user
        
        if not task:
            raise Http404
        
        task = Templates.objects.get(id = task)
        task_log_id = base.get_task_id()
        
        config = {
                    'project' : task.project.name,
                     'name' : str(task.name),
                     'target_type' : str(task.target_type),
                     'hosts' : str(task.hosts),
                     'threads' : str(task.threads),
                     'is_backup' : str(task.is_backup),
                     'backup_dir' : str(task.backup_dir),
                     'login_user' : str(task.login_user),
                     'addition_args' : str(task.addition_args),
                     'source_dir' : str(task.source_dir),
                     'temporary_dir' : str(task.temporary_dir),
                     'target_dir' : str(task.target_dir),
                     'exclude_files' : str(task.exclude_files),
                     'after_operations' : str(task.after_operations),
                 }
        
        task_log = Task_logs(
                                 task_log_id = task_log_id,
                                 template = task,
                                 config = config,
                                 add_time = add_time,
                                 oper_user = oper_user,
                                 status_code = status_code,
                             )
            
        raw_json = {'status' : 'success'} if task_log.save() == None else {'status' : 'failed'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@login_required
@csrf_protect    
def task_in_process(request):
    po = request.REQUEST
    page = po.get('page', '')
    rows = po.get('rows', '')
    r_from, r_end = base.sum_page_from_to_end(page, rows)
    tasks = Task_logs.objects.extra(where = ['status_code not in (4, 5)'])[r_from:r_end]
#    tasks = Task_logs.objects.all()
    task_total = tasks.count()
    t_list = []
    
    for task in tasks:
        r = {'task-id' : task.id,
             'status-code' : task.status_code,
             'config' : task.config,
             'task-log-id' : task.task_log_id,
             'task-target' : task.template.name,
             'operate-user' : task.oper_user.username,
             'add-time' : str(task.add_time),
             'start-time' : str(task.start_time),
             }
        t_list.append(r)
        
    raw_json = {'total' : task_total, 'rows' : t_list}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@login_required
@csrf_protect    
def list_task_log(request):
    po = request.REQUEST
    page = po.get('page', '')
    rows = po.get('rows', '')
    r_from, r_end = base.sum_page_from_to_end(page, rows)
    tasks = Task_logs.objects.extra(where = ['status_code in (4, 5)'])[r_from:r_end]
#    tasks = Task_logs.objects.all()
    task_total = tasks.count()
    t_list = []
    
    for task in tasks:
        r = {'task-id' : task.id,
             'status-code' : task.status_code,
             'config' : task.config,
             'task-log-id' : task.task_log_id,
             'task-target' : task.template.name,
             'operate-user' : task.oper_user.username,
             'add-time' : str(task.add_time),
             'end-time' : str(task.end_time),
             'start-time' : str(task.start_time),
             }
        t_list.append(r)
        
    raw_json = {'total' : task_total, 'rows' : t_list}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

def parse_config(task_id):
    task = Task_logs.objects.get(id = task_id)
    config = eval(task.config)
    
    return_config = {}
    ips = []
    if config['target_type'] == '1':
        project = Templates.objects.get(id = task.template.id).project.id
        total_ip = Relations.objects.filter(project = project, relation_type =  1)
        for h in total_ip:
            x = []
            ip = h.pro_ip.ip
            login_name = h.pro_ip.servers.login_name
            host = login_name + '@' + ip
            x.append(host)
            host_name = h.pro_ip.servers.hostname
            x.append(host_name)
            ips.append(x)

    else:
        r = config['hosts']
        ip_ids = r.split(',')
        total_ip = IPs.objects.filter(pk__in = ip_ids)
        for h in total_ip:
            x = []
            ip = h.ip
            login_name = h.servers.login_name
            host = login_name + '@' + ip
            x.append(host)
            host_name = h.servers.hostname
            x.append(host_name)
            ips.append(x)
    t = {}
    t['do_hosts'] = ips
    return_config = dict(t, **config)
    
    return return_config


@login_required
@csrf_protect
def get_detail_msg(request):
    task_id = request.REQUEST.get('task-log-id', '')
    
    if not task_id:
        raise Http404
    
    task_logs = Task_logs.objects.get(id = task_id)
    raw_json = {'data' : task_logs.status}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
    


@login_required
@csrf_protect
def start_process(request):
    task_id = request.REQUEST.get('task-log-id', '')
    
    if not task_id:
        raise Http404
    
    config = parse_config(task_id)
    config['task_id'] = task_id
    re = start_deploy.delay(config)
    tlog = Task_logs.objects.get(id = task_id)
    tlog.job_id = re
    
    raw_json = {'status' : 'success'} if tlog.save() == None else {'status' : 'failed'}
    
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@login_required
@csrf_protect
def pause_process(request):
    pass

@login_required
@csrf_protect
def restart_process(request):
    pass

@login_required
@csrf_protect
def continue_process(request):
    pass

@login_required
@csrf_protect
def end_process(request):
    task_log_id = request.REQUEST.get('task-log-id', '')
    if not task_log_id:
        raise Http404
    
    tlog = Task_logs.objects.get(id = task_log_id)
    tlog.status_code = 5
    raw_json = {'status' : 'success'} if tlog.save() == None else {'status' : 'failed'}
    
    return HttpResponse(json.dumps(raw_json), content_type="application/json")
    

@login_required
@csrf_protect
def stop_process(request):
    task_log_id = request.REQUEST.get('task-log-id', '')
    if not task_log_id:
        raise Http404
    
    jid = Task_logs.objects.get(id = task_log_id).job_id
    x = app.control.revoke(jid, terminate=True)
    return HttpResponse(x)

        
    
    
    
    
    
    
    
    
    
    
    
    
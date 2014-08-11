#coding: utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.views.decorators.csrf import csrf_protect
import ommp.deploy.base as base
import json

def index(request):
    return render_to_response('test.html')

def deploy_index(request):
    if request.method == 'POST':
        return render_to_response('index.html')
    else: return render_to_response('index.html')
    
def welcome(request):
    return render_to_response('welcome.html')

def side(request):
    return render_to_response('side.html')

@csrf_protect
def deploy(request):
    if request.method == 'POST':
        '''handle deploy method'''
        val = base.GetPostValve(request.POST)
        project = val['project']
        
        conf = base.get_config(project)
        if conf is None:
            raise Http404
        
        hosts = conf['hosts']
        
        deploy_type = val['type']
        out = ''
        if deploy_type == 'pre-deploy':
            command = base.GetCommand(deploy_type, conf = conf)
            out, stderr = base.local(command)
            
        elif deploy_type == 'official':
            port, username, password = base.GetGeneralInfo()
            if not hosts:
                return HttpResponse('该项目暂不支持正式发布!')
            
            for host in hosts:
                command = base.GetCommand(deploy_type, conf, host)
                channel = base.GetChannel(host, port, username, password)
                base.sudo(channel, 'chown %s:%s %s -R' % (username, username, conf['target']))
                stdout, stderr = base.local(command)
                base.sudo(channel, 'chmod 770 %s -R' % (conf['target']))
                done = 'Done!' if stderr == '' else ''
                out += '%s %s %s\n\n' % (host, stderr, done)
        return HttpResponse(out)
        
    elif request.method == 'GET':
        return render_to_response('deployment.html', context_instance=RequestContext(request))
    
@csrf_protect
def view_logs(request):
    '''
    hand log view request
    '''
    import ommp.functions.base as fb
    if request.method == 'POST':
        action = request.POST.get('action', '')
        project = request.POST.get('project', '')
        
        host = fb.get_config(project)['host']
        username = fb.get_connection_info()['username']
        password = fb.get_connection_info()['password']
        port = fb.get_connection_info()['port']
        
        if action == '':
            raise Http404
        
        elif action == 'getlist':
            channel = base.GetChannel(host, port, username, password)
            o = fb.get_log_list(channel, project)
            o = [i.replace("\n", "") for i in o]
            channel.close()
            return HttpResponse(json.dumps(o), content_type="application/json")
        
        elif action == 'getcontent':
            viewtype = request.POST.get('viewtype')
            filename = request.POST.get('filename', '')
            tempfile = "/tmp/" + filename
            if viewtype == 'dumps':
                channel = base.GetChannel(host, port, username, password)
                o = fb.get_log_content(channel, project, filename)
                channel.close()
                return HttpResponse(o)
            elif viewtype == 'realtime':
                wor = request.POST.get('wor', '')
                channel = base.GetChannel(host, port, username, password)
                if wor == 'w':
                    write = fb.WatchLogs(channel, wor, project, filename, tempfile)
                    write.run()
                elif wor == 'r':
                    read = fb.WatchLogs(channel, wor, project, filename, tempfile)
                    out = read.run()
                    return HttpResponse(out)

            return HttpResponse(viewtype)
        
    else: return render_to_response('logs.html', context_instance=RequestContext(request))
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import json
import ommp.resources.base as base
from ommp.models import Projects, Relations, IPs
import salt.client as client

def exc_command(request):
    return render_to_response('exc-command.html', context_instance=RequestContext(request))

@login_required
@csrf_protect
def handler_command(request):
    po = request.REQUEST
    pro = po.get('exec-project', '')
    servers = po.getlist('exec-server')
    command = po.get('exc-command', '')
    
    if not base.check_post_val(command):
        raise Http404
    command = command.strip()
    
    if pro and int(pro) != -1:
        ips = Relations.objects.filter(project = pro, relation_type = 1)
        hosts = []
        for ip in ips:
            host = ip.pro_ip.servers.hostname
            hosts.append(host)
        cl = client.LocalClient()
        try:
            re = cl.cmd(hosts,'cmd.run',[command],expr_form='list')[host]
        except:
            re = 'Not Return'
        
        raw_str = []
        for ip in ips:
            host = ip.pro_ip.servers.hostname
            r = {'exec-host-name' : host,
                 'exec-ip' : ip.pro_ip.ip,
                 'exec-result' : re,
                 'exec-idc' : ip.pro_ip.idc.idc_name,
                 }
            raw_str.append(r)
            
        return HttpResponse(json.dumps(raw_str), content_type="application/json")
    
    else:
        ips = IPs.objects.filter(pk__in = servers)
        hosts = []
        for ip in ips:
            host = ip.servers.hostname
            hosts.append(host)
        cl = client.LocalClient()
        re = cl.cmd(hosts,'cmd.run',[command],expr_form='list')
        
        raw_str = []
        for ip in ips:
            host = ip.servers.hostname
            r = {'exec-host-name' : host,
                 'exec-ip' : ip.ip,
                 'exec-result' : re[host],
                 'exec-idc' : ip.idc.idc_name,
                 }
            raw_str.append(r)
            
        return HttpResponse(json.dumps(raw_str), content_type="application/json")
        
    
    
    
    
    
    
    
    
    
    
    
    
#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import json
import ommp.resources.base as base
from ommp.models import Projects, Relations, IPs

def listpro(request):
    return render_to_response('projects.html', context_instance=RequestContext(request))

@csrf_protect
@login_required
def add_project(request):
    po = request.REQUEST
    admin = po.get('pro-admin', '')
    comment = po.get('pro-comment', '')
    description = po.get('pro-description', '')
    environment = po.get('pro-environment', '')
    language = po.get('pro-language', '')
    name = po.get('pro-name', '')
    repository = po.get('pro-repository', '')
    
    if not base.check_post_val(admin, description, environment, language, name, repository):
        raise Http404
    
    if not comment:
        comment = None
        
    add_date = base.get_now_date()
    
    pro = Projects(name = name,
                   desc = description,
                   admin = admin,
                   add_date = add_date,
                   repo = repository,
                   language = language, 
                   environment = environment,
                   comment = comment,
                   )
    raw_json = {'status' : 'success'} if pro.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def update_project(request):
    po = request.REQUEST
    admin = po.get('pro-admin', '')
    comment = po.get('pro-comment', '')
    description = po.get('pro-description', '')
    environment = po.get('pro-environment', '')
    language = po.get('pro-language', '')
    name = po.get('pro-name', '')
    repository = po.get('pro-repository', '')
    pro = po.get('pro-id', '')
    
    if not base.check_post_val(admin, description, environment, language, name, repository, pro):
        raise Http404
    
    if not comment:
        comment = None
        
    pro = Projects.objects.get(id = pro)
    
    pro.name = name
    pro.desc = description
    pro.admin = admin
    pro.repo = repository
    pro.language = language
    pro.environment = environment
    pro.comment = comment
    raw_json = {'status' : 'success'} if pro.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def list_projects(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    list_type = request.REQUEST.get('list_type', '')
    pro_list = []
    if list_type:
        pros = Projects.objects.all().values_list('id', 'name')
        i = 0
        for pro in pros:
            x = {'id':pro[0], 'name':pro[1], 'selected' : 'true'} if i == 0 else {'id':pro[0], 'name':pro[1]}
            pro_list.append(x)
            i += 1
        
        return HttpResponse(json.dumps(pro_list), content_type="application/json")
    
    if page and rows:
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        total = Projects.objects.all().count()
        pros = Projects.objects.all()[r_from:r_end]
    
    for pro in pros:
        r = {'pro-id' : pro.id,
             'pro-name' : pro.name,
             'pro-description' : pro.desc,
             'pro-admin' : pro.admin,
             'add-date' : pro.add_date,
             'pro-repository' : pro.repo,
             'pro-language' : pro.language,
             'pro-environment' : pro.environment,
             'pro-comment' : pro.comment,
             'pro-servers' : str(Relations.objects.filter(relation_type = 1, project = pro.id).count()) + ' 台'
             }
        pro_list.append(r)
    
    raw_json = {'total' : total, 'rows' : pro_list}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def delete_project(request):
    pro = request.REQUEST.get('pri', '')
    if not pro:
        raise Http404
    
    if Relations.objects.filter(relation_type = 1, project = pro).count() > 0:
        raw_json = {'status' : 'failed', 'data' : '该项目分配有服务器,请先清空服务器'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
    raw_json = {'status' : 'success'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")


@csrf_protect
@login_required
def add_pro_ip_relation(request):
    po = request.REQUEST
    ips = po.getlist('ips')
    pro_id = po.get('pro-id', '')
    comment = po.get('rel-comment', '')
    
    if not base.check_post_val(ips, pro_id):
        raise Http404
    
    if not comment:
        comment = None
    
    #get all ips which already in relation
    already_ip = Relations.objects.filter(project = pro_id)
    al_list = []
    for a in already_ip:
        al_list.append(str(a.pro_ip.id))
    new_list = []
    
    for x in ips:
        if str(x) not in al_list:
            new_list.append(x)
    
    status = True
    for ip in new_list:
        ip = IPs.objects.get(id = ip)
        project = Projects.objects.get(id = pro_id)
        rel = Relations(pro_ip = ip,
                        project = project,
                        relation_type = 1,
                        comment = comment,
                        )
        if rel.save() == None:
            pass
        else:
            status = False
            break
        
    raw_json = {'status' : 'success'} if status else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def list_pro_ip_relations(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    project = request.REQUEST.get('pro-id', '')
    if not project:
        raise Http404
    
    if page and rows:
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        total = Relations.objects.filter(project = project).count()
        rels = Relations.objects.filter(project = project)[r_from:r_end]
    
        pro_list = []
        for rel in rels:
            r = {'rel-id' : rel.id,
                 'ip-name' : rel.pro_ip.ip,
                 'idc-name' : rel.pro_ip.idc.idc_name,
                 'rel-comment' : rel.comment,
                 }
            pro_list.append(r)
    
    
        
        raw_json = {'total' : total, 'rows' : pro_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def del_pro_ip_relation(request):
    rel_id = request.REQUEST.get('rel-id', '')
    del_type = request.REQUEST.get('del-type', '')
    
    if not rel_id:
        raise Http404
    
    if del_type:
        if int(del_type) == 0:
            r = Relations.objects.get(id = rel_id)
            raw_json = {'status' : 'success'} if r.delete() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
        elif int(del_type) == 1:
            r = Relations.objects.get(id = rel_id).project.id
            raw_json = {'status' : 'success'} if Relations.objects.filter(relation_type = 1, project = r).delete() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
            
    


        






















    
#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import json
import base
from ommp.models import IDCs, Cabinets, Servers
import datetime

@csrf_protect
def add_idc(request):
    if request.method == 'POST':
        val = base.get_post_val(request.POST)
        idc_name = val['idc_name']
        address = val['provinces'] + val['city'] + val['county'] + val['address']
        contact = val['contact']
        phone_num = val['phone']
        email = val['email']
        zipcode = val['zipcode']
        display_addr = val['provinces'] + val['city']
        add_time = base.get_datetime()
        end_date = val['end_date']
        idc = IDCs(idc_name = idc_name,
                   address = address,
                   display_addr = display_addr,
                   contact = contact,
                   phone_num = phone_num,
                   email = email,
                   code = zipcode,
                   add_time = add_time,
                   end_date = end_date,
                   )
        
        idc.save()
        if idc.id:  
            return HttpResponse(base.dump_json(0), content_type="application/json")
        else:
            return HttpResponse(base.dump_json(1), content_type="application/json")
    else: return HttpResponse("xxx")
    
def list_idc(request):
    idcs = IDCs.objects.all()
    return render_to_response('idcs.html', {'top_title' : '机房管理', 'idcs' : idcs}, context_instance=RequestContext(request))

@csrf_protect
def get_idcs(request):
    idcid = request.REQUEST.get('idcid','')
    idcs = IDCs.objects.all().values_list('id', 'idc_name')
    i = []
    n = 0
    if not idcid:
        for idc in idcs:
            x = {'id':idc[0], 'name':idc[1], 'selected' : 'true'} if n == 0 else {'id':idc[0], 'name':idc[1]}
            n += 1
            i.append(x)
    else:
        for idc in idcs:
            x = {'id':idc[0], 'name':idc[1], 'selected' : 'true'} if str(idc[0]) == idcid else {'id':idc[0], 'name':idc[1]}
            i.append(x)
    return HttpResponse(json.dumps(i), content_type="application/json")

@csrf_protect
@login_required
def get_users(request):
    uid = request.REQUEST.get('uid','')
    users = User.objects.values_list('id', 'username')
    i = []
    n = 0
    if not uid:
        for user in users:
            x = {'id' : user[0], 'username' : user[1], 'selected' : 'true'} if n == 0 else {'id' : user[0], 'username' : user[1]}
            n += 1
            i.append(x)
    else:
        for user in users:
            x = {'id' : user[0], 'username' : user[1], 'selected' : 'true'} if str(user[0]) == uid else {'id' : user[0], 'username' : user[1]}
            i.append(x)
    return HttpResponse(json.dumps(i), content_type="application/json")

@csrf_protect
def get_idc_detail(request):
    if request.method == 'POST':
        idc_id = request.POST.get('idc-id', '')
        if idc_id == '':
            raise Http404
        
        idc_info = IDCs.objects.get(id = idc_id)
        items = {'id' : idc_info.id,
                 'address' : idc_info.address,
               'zipcode' : idc_info.code,
               'contact' : idc_info.contact,
               'phone' : idc_info.phone_num,
               'email' : idc_info.email,
               'idc_name' : idc_info.idc_name,
               'end_date' : idc_info.end_date,
               }
        return HttpResponse(json.dumps(items), content_type="application/json")
    
@csrf_protect
def update_idc_info(request):
    if request.method == 'POST':
        val = base.get_post_val(request.POST)
        idc_id = val['idc_id']
        
        idc_name = val['idc_name']
        address = val['address']
        contact = val['contact']
        phone_num = val['phone']
        email = val['email']
        zipcode = val['zipcode']
        add_time = base.get_datetime()
        end_date = val['end_date']
        idc = IDCs.objects.get(id = idc_id)
        
        idc.idc_name = idc_name
        
        idc.address = address
        idc.contact = contact
        idc.phone_num = phone_num
        idc.email = email
        idc.code = zipcode
        idc.add_time = add_time
        idc.end_date = end_date
        
        idc.save()
        if idc.id:  
            return HttpResponse(base.dump_json(0), content_type="application/json")
        else:
            return HttpResponse(base.dump_json(1), content_type="application/json")
    else: return HttpResponse("xxx")

@csrf_protect
def del_idc(request):

    if request.method == 'POST':
        idc_id = request.POST.get('idc-id', '')
        if idc_id:
            idc = IDCs.objects.get(id = idc_id)
            raw_json = {'status' : 'success'} if idc.delete() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
            
            
            
            
#action about server 
def servers(request):
    return render_to_response('servers.html', context_instance=RequestContext(request))

@csrf_protect
@login_required
def add_server(request):
    if request.method == 'POST':
        po = request.POST
    else:raise Http404
    
    name = po.get('svr-name', '')
    idc = po.get('svr-add-idc', '')
    cabinets = po.get('svr-add-cab', '')
    size = po.get('svr-size', '')
    parts = po.get('svr-parts', '')
    add_date = base.get_now_date()
    end_date = po.get('svr-end-date', '')
    father = po.get('svr-add-father', '')
    used_type = po.get('svr-add-usable', '')
    admin = po.get('svr-add-admin', '')
    os = po.get('svr-add-os', '')
    
    father = Servers.objects.get(id = father) if father else None
        
    if not base.check_post_val(name, idc, cabinets, size, parts, end_date, used_type, admin, os):
        raise Http404
    
    idc = IDCs.objects.get(id = idc)
    cabinets = Cabinets.objects.get(id = cabinets)
    admin = User.objects.get(id = admin)
    
    svr = Servers(name = name,
                  idc = idc,
                  cabinets = cabinets,
                  size = size,
                  add_date = add_date,
                  parts = parts,
                  end_date = end_date,
                  father = father,
                  used_type = used_type,
                  admin = admin,
                  os = os,
                  )
    raw_json = {'status' : 'success'} if svr.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
    
@csrf_protect
@login_required
def update_server(request):
    if request.method == 'POST':
        po = request.POST
    else:raise Http404
    
    svr_id = po.get('svr-id', '')
    name = po.get('svr-name', '')
    idc = po.get('svr-update-idc', '')
    cabinets = po.get('svr-update-cab', '')
    size = po.get('svr-size', '')
    parts = po.get('svr-parts', '')
    end_date = po.get('svr-end-date', '')
    father = po.get('svr-update-father', '')
    used_type = po.get('svr-update-usable', '')
    admin = po.get('svr-update-admin', '')
    os = po.get('svr-update-os', '')
    
    father = Servers.objects.get(id = father) if father else None
        
    if not base.check_post_val(svr_id, name, idc, cabinets, size, parts, end_date, used_type, admin, os):
        raise Http404
    
    idc = IDCs.objects.get(id = idc)
    cabinets = Cabinets.objects.get(id = cabinets)
    admin = User.objects.get(id = admin)
    
    svr = Servers.objects.get(id = svr_id)
    
    svr.name = name
    svr.idc = idc
    svr.cabinets = cabinets
    svr.size = size
    svr.parts = parts
    svr.end_date = end_date
    svr.father = father
    svr.used_type = used_type
    svr.admin = admin
    svr.os = os
    
    raw_json = {'status' : 'success'} if svr.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")


@csrf_protect
@login_required
def get_servers(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    father_id = request.REQUEST.get('fid', '')
    cab = request.REQUEST.get('cab', '')

    cb_list = []

    if cab:
        if father_id:
            if int(father_id) != 0:
                svrs = Servers.objects.filter(cabinets = cab)
                for svr in svrs:
                    c = {'id' : svr.id, 'name' : svr.name, 'selected' : 'true'} if svr.id == int(father_id) else {'id' : svr.id, 'name' : svr.name, }
                    cb_list.append(c)
                return HttpResponse(json.dumps(cb_list), content_type="application/json")
            else:
                n = 0
                svrs = Servers.objects.filter(cabinets = cab)
                for svr in svrs:
                    c = {'id' : svr.id, 'name' : svr.name, }
                    cb_list.append(c)
                    n += 1
                return HttpResponse(json.dumps(cb_list), content_type="application/json")
        n = 0
        svrs = Servers.objects.filter(cabinets = cab)
        for svr in svrs:
            c = {'id' : svr.id, 'name' : svr.name, 'selected' : 'true'} if n == 0 else {'id' : svr.id, 'name' : svr.name}
            cb_list.append(c)
            n += 1
        return HttpResponse(json.dumps(cb_list), content_type="application/json")

    if page and rows:
        page = int(page)
        rows = int(rows)
        r_from = (page - 1) * rows
        
        svrs = Servers.objects.all()[r_from:r_from + rows]
        cb_total = Servers.objects.count()
        for svr in svrs:
            svr_father = "无" if svr.father == None else svr.father.name
            father_id = '0' if svr.father == None else svr.father.id
            type = svr.used_type
            if type == 0:
                used_type = '测试'
            elif type == 1:
                used_type = '生产'
            elif type == 2:                             
                used_type = '不可用'               
                
            r = {'svr-id' : svr.id,
                 'cab-id' : svr.cabinets.id,
                 'admin-id' : svr.admin.id,
                 'svr-used-type' : svr.used_type,
                 'idc-id' : svr.idc.id,
                 'father-id' : father_id,
                 'svr-name' : svr.name,
                 'idc-name' : svr.idc.idc_name,
                 'cab-name' : svr.cabinets.name,
                 'svr-size' : svr.size,
                 'svr-parts' : svr.parts,
                 'svr-os' : svr.os,
                 'storage-date' : svr.add_date,
                 'end-date' : svr.end_date,
                 'svr-father' : svr_father,
                 'svr-usable' : used_type,
                 'admin-name' : svr.admin.username,
                 'idc-id' : svr.idc.id,
                 }
            cb_list.append(r)
        raw_json = {'total' : cb_total, "rows" : cb_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required   
def del_server(request):
    sid = request.REQUEST.get('sid', '')
    if not sid:
        raise Http404
    
    if Servers.objects.filter(father = sid).count() > 0:
        raw_json = {'status' : 'failed', 'data' : 'Have child, can\'t delete'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
    raw_json = {'status' : 'success'} if Servers.objects.filter(id = sid).delete() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

#action about cabinets
def cabinets(request):
    return render_to_response('cabinets.html', context_instance=RequestContext(request))

@csrf_protect
@login_required
def add_cabinet(request):
    if request.method == 'POST':
        po = request.POST
        name = po.get('cb-name', '')
        idc = po.get('cb-add-idc', '')
        admin = po.get('cb-add-admin', '')
        size = po.get('cb-size', '')
        add_date = base.get_now_date()
        end_date = po.get('cb-end-date', '')
        servers = 0
        available = po.get('cb-add-usable', '')
        
        if not base.check_post_val(name, idc, admin, size, end_date, available):
            raise Http404
        idc = IDCs.objects.get(id = idc)
        admin = User.objects.get(id = admin)
        
        cb = Cabinets(name = name,
                      idc = idc,
                      admin = admin,
                      size = size,
                      add_date = add_date,
                      end_date = end_date,
                      servers = servers,
                      available = available)
        
        raw_json = {'status' : 'success'} if cb.save() == None else {'status' : 'failed'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def del_cabinet(request):
    if request.method == 'POST':
        cid = request.POST.get('cid', '')
        if cid:
            raw_json = {'status' : 'success'} if Cabinets.objects.filter(id = cid).delete() == None else {'status' : 'failed'}
            
    return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def update_cabinet(request):
    if request.method == 'POST':
        po = request.POST
        id = po.get('cb-id', '')
        name = po.get('cb-name', '')
        idc = po.get('cb-update-idc', '')
        admin = po.get('cb-update-admin', '')
        size = po.get('cb-size', '')
        end_date = po.get('cb-end-date', '')
        available = po.get('cb-update-usable', '')
        
        if not base.check_post_val(name, idc, admin, size, end_date, available):
            raise Http404

        cb = Cabinets.objects.get(id = id)
        idc = IDCs.objects.get(id = idc)
        admin = User.objects.get(id = admin)
        
        cb.name = name
        cb.idc = idc
        cb.admin = admin
        cb.size = size
        cb.end_date = end_date
        cb.available = available
        
        raw_json = {'status' : 'success'} if cb.save() == None else {'status' : 'failed'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def get_cabinets(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    idc = request.REQUEST.get('idcid', '')
    cabid = request.REQUEST.get('cabid','')

    cb_list = []
    if idc:
        if cabid:
            cabs = Cabinets.objects.filter(idc = idc).values_list('id', 'name')
            for cab in cabs:
                c = {'id' : cab[0], 'name' : cab[1], 'selected' : 'true'} if cab[0] == int(cabid) else {'id' : cab[0], 'name' : cab[1]}
                cb_list.append(c)
            return HttpResponse(json.dumps(cb_list), content_type="application/json")
        else:
            n = 0
            cabs = Cabinets.objects.filter(idc = idc).values_list('id', 'name')
            for cb in cabs:
                c = {'id' : cb[0], 'name' : cb[1], 'selected' : 'true'} if n == 0 else {'id' : cb[0], 'name' : cb[1]}
                cb_list.append(c)
                n += 1
            return HttpResponse(json.dumps(cb_list), content_type="application/json")
    
    if page and rows:
        page = int(page)
        rows = int(rows)
        r_from = (page - 1) * rows
        cbs = Cabinets.objects.all()[r_from:r_from + rows]
        cb_total = Cabinets.objects.count()
        for cb in cbs:
            is_full = '有' if cb.available == 0 else '无'
            c = {"cb-name" : cb.name,
                 'idc-name' : cb.idc.idc_name,
                 'cb-size' : cb.size,
                 'storage-date' : cb.add_date,
                 'end-date' : cb.end_date,
                 'sum-servers' : cb.servers,
                 'is-full' : is_full,
                 'op-name' : cb.admin.username,
                 'cb-id' : cb.id,
                 'idc-id' : cb.idc.id,
                 'user-id' : cb.admin.id,
                 'cb-usable' : cb.available
                 }
            cb_list.append(c)
        raw_json = {'total' : cb_total, "rows" : cb_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")

def get_usable(request):
    usable = request.REQUEST.get('ub', '')
    cid = request.REQUEST.get('cid', '')
    raw_json = []
    if cid:
        cab = Cabinets.objects.get(id = cid)
    else:
        return Http404
    if usable:
        ub = cab.available
        if str(ub) == usable and ub == 0:
            raw_json = [{'id' : '0', 'usable' : '有', 'selected' : 'true'},{'id' : '1', 'usable' : '无'}]
        else:
            raw_json = [{'id' : '0', 'usable' : '有'},{'id' : '1', 'usable' : '无', 'selected' : 'true'}]
            
    return HttpResponse(json.dumps(raw_json), content_type="application/json")



#action about ipaddr
def ipaddr(request):
    return render_to_response('ipaddr.html', context_instance=RequestContext(request))




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
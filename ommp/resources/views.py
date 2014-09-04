#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import json
import base
from ommp.models import IDCs, Cabinets
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
        add_date = datetime.date.today().strftime('%m/%d/%Y')
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
        
        raw_json = {'status' : 'success'} if cb.save() > 0 else {'status' : 'failed'}
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
    cbs = Cabinets.objects.all()
    cb_total = 0
    cb_list = []
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
        cb_total += 1
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




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
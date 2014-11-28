#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import json
import base
import os
from ommp.models import IDCs, Cabinets, Servers, IPs, Projects, Relations
import xlrd


@csrf_protect
def add_idc(request):
    if request.method == 'POST':
        val = base.get_post_val(request.POST)
        idc_name = val['idc_name']
        address = val['provinces'] + val['city'] + val['county'] + val['address']
        contact = val['contact']
        cellphone_num = val['cellphone_num']
        phone_num = val['phone_num']
        email = val['email']
        zipcode = val['zipcode']
        display_addr = val['provinces'] + val['city']
        add_time = base.get_datetime()
        end_date = val['end_date']
        idc = IDCs(idc_name = idc_name,
                   address = address,
                   display_addr = display_addr,
                   contact = contact,
                   cellphone_num = cellphone_num,
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
    return render_to_response('idcs.html', context_instance=RequestContext(request))

@login_required
@csrf_protect
def get_idcs(request):
    idcid = request.REQUEST.get('idcid','')
    idcs = IDCs.objects.all().values_list('id', 'idc_name')
    i = []
    if not idcid:
        for idc in idcs:
            x = {'id':idc[0], 'name':idc[1]}
            i.append(x)
    else:
        for idc in idcs:
            x = {'id':idc[0], 'name':idc[1], 'selected' : 'true'} if str(idc[0]) == idcid else {'id':idc[0], 'name':idc[1]}
            i.append(x)
    return HttpResponse(json.dumps(i), content_type="application/json")

@login_required
@csrf_protect
def list_idcs(request):
    idcs = IDCs.objects.all()
    total = idcs.count()
    idc_list = []
    for idc in idcs:
        r = {'idc-id' : idc.id,
             'idc-name' : idc.idc_name,
             'idc-address' : idc.address,
             'idc-contacts' : idc.contact,
             'cellphone-num' : idc.cellphone_num,
             'phone-num' : idc.phone_num,
             'email-addr' : idc.email,
             'end-date' : idc.end_date,
             'idc-post' : idc.code,
             }
        
        idc_list.append(r)
        
    raw_json = {'total' : total, 'rows' : idc_list}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@login_required
@csrf_protect
def modify_addr(request):
    po = request.REQUEST
    idc_id = po.get('idc-id', '')
    provinces = po.get('provinces', '')
    county = po.get('county', '')
    city = po.get('city', '')
    address = po.get('address', '')
    zipcode = po.get('zipcode', '')
    if not idc_id:
        raise Http404
    idc = IDCs.objects.get(id = idc_id)
    

    idc.display_addr = provinces + '-' + city + '-' + county + '-' + address
    idc.code = zipcode
        
    raw_json = {'status' : 'success'} if idc.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@login_required
@csrf_protect
def idc_summary(request):
    idc_id = request.REQUEST.get('idc-id', '')
    
    if not idc_id:
        raise Http404
    
    record_list = []
#    cabinets = {'resource-name' : '机柜',
#                'total-num' : Cabinets.objects.filter(idc = idc_id).count(),
#                'be-used' : '-1',
#                'available-num' : '-1',
#                'other-num' : '-1',
#                }
#    record_list.append(cabinets)
    
    other_num = Servers.objects.filter(idc = idc_id, used_type = 2).count()
    total_num = Servers.objects.filter(idc = idc_id).count()
    available_num = Servers.objects.filter(idc = idc_id, used_type = 3).count()
    be_used =  total_num - other_num - available_num
    servers = {'resource-name' : '服务器',
                'total-num' : total_num,
                'be-used' : be_used,
                'available-num' : available_num,
                'other-num' : other_num,
                }
    record_list.append(servers)
    
    be_used = IPs.objects.filter(idc = idc_id, status = 2).count()
    total_num = IPs.objects.filter(idc = idc_id).count()
    available_num = IPs.objects.filter(idc = idc_id, status = 0).count()
    other_num = total_num - available_num - be_used
    ips = {'resource-name' : 'IP Addr',
                'total-num' : total_num,
                'be-used' : be_used,
                'available-num' : available_num,
                'other-num' : other_num,
                }
    record_list.append(ips)
        
    raw_json = {'total' : '3', 'rows' : record_list}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def get_users(request):
    uid = request.REQUEST.get('uid','')
    users = User.objects.values_list('id', 'username')
    i = []
    n = 0
    if not uid:
        for user in users:
            x = {'id' : user[0], 'username' : user[1]}
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
    po = request.REQUEST
    idc_id = po.get('idc-id', '')
    cellphone = po.get('cellphone-num', '')
    concatcs = po.get('contact', '')
    email = po.get('email', '')
    end_date = po.get('end-date', '')
    idc_name = po.get('idc-name', '')
    phone = po.get('phone-num', '')

    idc = IDCs.objects.get(id = idc_id)
    
    idc.idc_name = idc_name
    
    idc.contact = concatcs
    idc.cellphone_num = cellphone
    idc.phone_num = phone
    idc.email = email
    idc.end_date = end_date
    
    raw_json = {'status' : 'success'} if idc.save() == None else {'status' : 'failed'}
    
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

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
#    cabinets = po.get('svr-add-cab', '')
    size = po.get('svr-size', '')
    parts = po.get('svr-parts', '')
    add_date = base.get_now_date()
    end_date = po.get('svr-end-date', '')
    father = po.get('svr-add-father', '')
    used_type = po.get('svr-add-usable', '')
    admin = po.get('svr-add-admin', '')
    os = po.get('svr-add-os', '')
    hostname = po.get('svr-add-hostname', '')
    username = po.get('svr-add-username', '')
    
    father = Servers.objects.get(id = father) if father else None
        
    if not base.check_post_val(name, idc, size, parts, used_type, admin, os, hostname, username):
        raise Http404
    
    idc = IDCs.objects.get(id = idc)
    admin = User.objects.get(id = admin)
    
    svr = Servers(name = name,
                  idc = idc,
                  size = size,
                  add_date = add_date,
                  parts = parts,
                  end_date = end_date,
                  father = father,
                  used_type = used_type,
                  admin = admin,
                  os = os,
                  hostname = hostname,
                  login_name = username,
                  )
    raw_json = {'status' : 'success'} if svr.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required    
def import_server(request):
    f = request.FILES.get('import-file', None)
    x = handle_uploaded_file(f)
    
    book = xlrd.open_workbook(x)
    table = book.sheet_by_index(0)
    rows = table.nrows

    status = True
    error_list = []
    
    for r in range(0, rows):
        row = table.row(r)
#        return HttpResponse(row[11].value)
        server = Servers(name = row[0].value,
                         idc = IDCs.objects.get(id = row[1].value),
                         size = row[2].value,
                         parts = row[3].value,
                         os = row[4].value,
                         hostname = row[5].value,
                         login_name = row[6].value,
                         add_date = row[7].value,
                         end_date = row[8].value,
                         father = None,
                         used_type = row[10].value,
                         admin = User.objects.get(id = row[11].value),
                         )
        if server.save() != None:
            status = False
            error_list.append(r + 1)
            
    raw_json = '导入成功，请刷新该页查看' if status else '如下行未导入成功 %s' % error_list
    
    return HttpResponse(raw_json)

def handle_uploaded_file(f):
    file_name = ""

    try:
        path = "/tmp/ommp/"
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = path + f.name
        if os.path.isfile(file_name):
            os.remove(file_name)
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception, e:
        print e

    return file_name
    
    
@csrf_protect
@login_required
def update_server(request):
    if request.method == 'POST':
        po = request.POST
    else:raise Http404
    
    svr_id = po.get('svr-id', '')
    name = po.get('svr-name', '')
    idc = po.get('svr-update-idc', '')
    size = po.get('svr-size', '')
    parts = po.get('svr-parts', '')
    end_date = po.get('svr-end-date', '')
    father = po.get('svr-update-father', '')
    used_type = po.get('svr-update-usable', '')
    admin = po.get('svr-update-admin', '')
    os = po.get('svr-update-os', '')
    hostname = po.get('svr-update-hostname', '')
    username = po.get('svr-update-username', '')
    
    father = Servers.objects.get(id = father) if father else None
        
    if not base.check_post_val(svr_id, name, idc, size, parts, end_date, used_type, admin, os, hostname, username):
        raise Http404
    
    idc = IDCs.objects.get(id = idc)
    admin = User.objects.get(id = admin)
    
    svr = Servers.objects.get(id = svr_id)
    
    svr.name = name
    svr.idc = idc
    svr.size = size
    svr.parts = parts
    svr.end_date = end_date
    svr.father = father
    svr.used_type = used_type
    svr.admin = admin
    svr.os = os
    svr.hostname = hostname
    svr.login_name = username
    
    raw_json = {'status' : 'success'} if svr.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def update_father_servers(request):
    po = request.REQUEST
    fa = po.get('father-id', '')
    idc_id = po.get('idc-id', '')
    svr_id = po.get('svr-id', '')

    if not (idc_id and svr_id):
        raise Http404
    
    svr = Servers.objects.get(id = svr_id)
    father = Servers.objects.get(id = fa) if fa else None
    svr.father = father
    
    raw_json = {'status' : 'success'} if svr.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")


@csrf_protect
@login_required
def get_father_servers(request):
    po = request.REQUEST
    idc = po.get('idc', '')
    svr_id = po.get('svrid', '')
    if not idc:
        raise Http404
    cb_list = []
    
    if svr_id:
        svrs = Servers.objects.filter(idc = idc)
        for svr in svrs:
            c = {'id' : svr.id, 'name' : svr.name, 'selected' : 'true'} if int(svr_id) == svr.id else {'id' : svr.id, 'name' : svr.name}
            cb_list.append(c)
        return HttpResponse(json.dumps(cb_list), content_type="application/json")
    else:
        svrs = Servers.objects.filter(idc = idc)
        for svr in svrs:
            c =  {'id' : svr.id, 'name' : svr.name}
            cb_list.append(c)
        return HttpResponse(json.dumps(cb_list), content_type="application/json")

@csrf_protect
@login_required
def get_servers(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    father_id = request.REQUEST.get('fid', '')
    idc = request.REQUEST.get('idc', '')
    
    cb_list = []
    
    if idc:
        svrs = Servers.objects.all().values_list('id', 'name')
        for svr in svrs:
            r = {'id' : svr[0],
                 'name' : svr[1],
                 }
            cb_list.append(r)
        return HttpResponse(json.dumps(cb_list), content_type="application/json")
            


    if page and rows:
        page = int(page)
        rows = int(rows)
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        
        svrs = Servers.objects.all()[r_from:r_end]
        cb_total = Servers.objects.count()
        for svr in svrs:
            svr_father = "无" if svr.father == None else svr.father.name
            father_id = '0' if svr.father == None else svr.father.id
                
            r = {'svr-id' : svr.id,
                 'admin-id' : svr.admin.id,
                 'svr-used-type' : svr.used_type,
                 'idc-id' : svr.idc.id,
                 'father-id' : father_id,
                 'svr-name' : svr.name,
                 'idc-name' : svr.idc.idc_name,
                 'svr-size' : svr.size,
                 'svr-parts' : svr.parts,
                 'svr-os' : svr.os,
                 'svr-hostname' : svr.hostname,
                 'storage-date' : svr.add_date,
                 'end-date' : svr.end_date,
                 'svr-father' : svr_father,
                 'svr-usable' : svr.used_type,
                 'admin-name' : svr.admin.username,
                 'idc-id' : svr.idc.id,
                 'svr-username' : svr.login_name,
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
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        cbs = Cabinets.objects.all()[r_from:r_end]
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

@csrf_protect
@login_required
def add_ips(request):
    if request.method == 'POST':
        po = request.POST
        ip_from = po.get('ip-from', '')
        ip_end = po.get('ip-end', '')
        add_type = po.get('add-type', '')
        netmask = po.get('netmask', '')
        idc = po.get('add-idc', '')
        ip_type = po.get('ip-type')
        
        if not base.check_post_val(ip_from, ip_end, add_type, netmask, idc, ip_type):
            raise Http404
        
        
        
        idc = IDCs.objects.get(id = idc)

        if add_type == '0':                                 #add one ip once time
            ip = IPs(ip = ip_from,
                      netmask = netmask,
                      idc = idc,
                      ip_type = ip_type,
                      status = '0',
                      )
            raw_json = {'status' : 'success'} if ip.save() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
            
        elif add_type == '1':
            ip_from = ip_from.split('.')
            ip_end = int(ip_end)
            status = True

            for i in range(int(ip_from[3]), ip_end + 1):
                ip = ip_from[0] + '.' + ip_from[1] + '.' + ip_from[2] + '.' + str(i)
                ips = IPs(ip = ip,
                          netmask = netmask,
                          idc = idc,
                          ip_type = ip_type,
                          status = 0,
                          )
                if ips.save() == None:
                    pass
                else:
                    status = False
                    break
            raw_json = {'status' : 'success'} if status else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
        
@csrf_protect
@login_required
def get_ips(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    ip_type = request.REQUEST.get('ip-type', '')
    idc = request.REQUEST.get('idc','')
    pri_ip_id = request.REQUEST.get('priid', '')
    status = request.REQUEST.get('status', '')
    ip_list = []
    
    if ip_type and idc:
        if status:
            ips = IPs.objects.filter(ip_type = ip_type, idc = idc, status = status)
            if not ips:
                pass
            for ip in ips:
                if pri_ip_id:
                    i = {'id' : ip.id,'name' : ip.ip, 'selected' : 'true'} if int(pri_ip_id) == ip.id else {'id' : ip.id,'name' : ip.ip}
                    ip_list.append(i)
                else:
                    i = {'id' : ip.id,'name' : ip.ip}
                    ip_list.append(i)
                    
            return HttpResponse(json.dumps(ip_list), content_type="application/json")
        else:
            ips = IPs.objects.filter(ip_type = ip_type, idc = idc)
            if not ips:
                pass
            for ip in ips:
                if pri_ip_id:
                    i = {'id' : ip.id,'name' : ip.ip, 'selected' : 'true'} if int(pri_ip_id) == ip.id else {'id' : ip.id,'name' : ip.ip}
                    ip_list.append(i)
                else:
                    i = {'id' : ip.id,'name' : ip.ip}
                    ip_list.append(i)
                    
            return HttpResponse(json.dumps(ip_list), content_type="application/json")
    if idc:
        ips = IPs.objects.filter(idc = idc, status = 2)
        x = 0
        if not ips:
            pass
        for ip in ips:
            i = {'id' : ip.id,'name' : ip.ip, 'selected' : 'true'} if x == 0 else {'id' : ip.id,'name' : ip.ip}
            x += 1
            ip_list.append(i)
            
        return HttpResponse(json.dumps(ip_list), content_type="application/json")
        
                
            
        
    
    if page and rows:
        page = int(page)
        rows = int(rows)
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        ips = IPs.objects.filter(ip_type = ip_type)[r_from:r_end]
        if not ips:
            pass
        cb_total = IPs.objects.filter(ip_type = ip_type).count()
        
        for ip in ips:
            if ip.status == 0:
                status = '可用'
            elif ip.status == 1:
                status = '禁用'
            else: status = '已使用'
            
            if ip.servers == None:
                svr_id = ''
                svr_name = ''
            else:
                svr_id = ip.servers.id
                svr_name = ip.servers.name
            
            if ip.project == None:
                pro_id = ''
                pro_name = ''
            else: 
                pro_id = ip.project.id
                pro_name = ip.project.name
                
            i = {'svr-id' : svr_id,
                 'idc-id' : ip.idc.id,
                 'ip-id' : ip.id,
                 'pro-id' : pro_id,
                 'ip-name' : ip.ip,
                 'idc-name' : ip.idc.idc_name,
                 'pro_name' : pro_name,
                 'svr-name' : svr_name,
                 'ip-comment' : ip.comment,
                 'status' : status,
                 }
            
            ip_list.append(i)
            
        raw_json = {'total' : cb_total, "rows" : ip_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def update_ip(request):
    if request.method == 'POST':
        po = request.POST
        
        comment = po.get('ip-up-comment', '')
        project = po.get('ip-up-pro-id', '')
        server = po.get('ip-up-svr-id', '')
        ip = po.get('up-ip-id', '')
        status = po.get('status', '')
        
        if not ip:
            raise Http404

        ip = IPs.objects.get(id = ip)
        
        if status and (int(status) == 1 or int(status) == 0):
            ip.status = status
            ip.project = None
            ip.servers = None
            ip.comment = comment
            raw_json = {'status' : 'success'} if ip.save() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")
                
            
        
        if project:
            ip.project = Projects.objects.get(id = project)

        if server:
            ip.servers = Servers.objects.get(id = server)
            ip.status = 2
            
        ip.comment = comment
        
        raw_json = {'status' : 'success'} if ip.save() == None else {'status' : 'failed'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")

                    
@csrf_protect
@login_required
def delete_ip(request):
    if request.method == 'POST':
        po = request.POST
        ip = po.get('ipid','')
        
        if ip:
            raw_json = {'status' : 'success'} if IPs.objects.get(id = ip).delete() == None else {'status' : 'failed'}
            return HttpResponse(json.dumps(raw_json), content_type="application/json")


#about ip relation

@csrf_protect
@login_required
def add_ip_relation(request):
    po = request.REQUEST
    pub_ip = po.get('ip-relation-add-pub', '')
    pub_port = po.get('ip-relation-add-pub-port', '')
    pri_ip = po.get('ip-relation-add-pri', '')
    pri_port = po.get('ip-relation-add-pri-port', '')
    comment = po.get('ip-up-comment', '')
    
    if not comment:
        comment = None
    
    if not base.check_post_val(pub_ip, pub_port, pri_ip, pri_port):
        raise 404
    check_str = pub_ip.strip() + pub_port.strip() + pri_ip.strip() + pri_port.strip()
    check_code = base.get_check_code(check_str)
    
    pub_ip = IPs.objects.get(id = pub_ip)
    pri_ip = IPs.objects.get(id = pri_ip)
    
    check_value = Relations.objects.filter(check_code = check_code).count()
    if check_value > 0:
            raw_json = {'status' : 'failed', 'data' : '已有相同映射,请查证再提交'} 
            return HttpResponse(json.dumps(raw_json), content_type="application/json") 
    
    rel = Relations(public_ip = pub_ip,
                    public_port = pub_port,
                    private_ip = pri_ip,
                    private_port = pri_port,
                    relation_type = 0,
                    comment = comment,
                    check_code = check_code
                    )
    raw_json = {'status' : 'success'} if rel.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def get_ip_relation(request):
    page = request.REQUEST.get('page', '')
    rows = request.REQUEST.get('rows', '')
    
    if page and rows:
        r_from, r_end = base.sum_page_from_to_end(page, rows)
        rel_total = Relations.objects.filter(relation_type = '0').count()
        rels = Relations.objects.filter(relation_type = '0')[r_from:r_end]

        rel_list = []
        for rel in rels:
            s = {'relation-id' : rel.id,
                 'pub-ip-id' : rel.public_ip.id,
                 'pri-ip-id' : rel.private_ip.id,
                 'pub-name' : rel.public_ip.ip,
                 'pub-port' : rel.public_port,
                 'pri-name' : rel.private_ip.ip,
                 'pri-port' : rel.private_port,
                 'ip-comment' : rel.comment,
                 'idc-id' : rel.public_ip.idc.id
                 }
            rel_list.append(s)

        raw_json = {'total' : rel_total, 'rows' : rel_list}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")

@csrf_protect
@login_required
def del_ip_relation(request):
    rel_id = request.REQUEST.get('rel-id')
    if rel_id:
        raw_json = {'status' : 'success'} if Relations.objects.get(id = rel_id).delete() == None else {'status' : 'failed'}
        return HttpResponse(json.dumps(raw_json), content_type="application/json")
    
@csrf_protect
@login_required
def update_ip_relation(request):
    po = request.REQUEST
    pub_ip = po.get('ip-pub-id', '')
    pub_port = po.get('ip-relation-update-pub-port', '')
    pri_ip = po.get('ip-pri-id', '')
    pri_port = po.get('ip-relation-update-pri-port', '')
    comment = po.get('ip-up-comment', '')
    rel_id = po.get('ip-relation-id', '')
    
    if not comment:
        comment = None
    
    if not base.check_post_val(pub_ip, pub_port, pri_ip, pri_port, rel_id):
        raise Http404
    check_str = pub_ip.strip() + pub_port.strip() + pri_ip.strip() + pri_port.strip()
    check_code = base.get_check_code(check_str)

    pub_ip = IPs.objects.get(id = pub_ip)
    pri_ip = IPs.objects.get(id = pri_ip)
    rel = Relations.objects.get(id = rel_id)

    rel.public_ip = pub_ip
    rel.public_port = pub_port
    rel.private_ip = pri_ip
    rel.private_port = pri_port
    rel.relation_type = 0
    rel.comment = comment
    rel.check_code = check_code
    raw_json = {'status' : 'success'} if rel.save() == None else {'status' : 'failed'}
    return HttpResponse(json.dumps(raw_json), content_type="application/json")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
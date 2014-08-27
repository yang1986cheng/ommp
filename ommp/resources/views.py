#coding: utf-8
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import json
import base
from ommp.models import IDCs

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
               'end_date' : 'idc_info.end_date',
               }
        return HttpResponse(json.dumps(items), content_type="application/json")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
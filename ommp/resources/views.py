#coding: utf-8
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import base
from ommp.models import IDCs

@csrf_protect
def add_idc(request):
    if request.method == 'POST':
        val = base.get_post_val(request.POST)
        idc_name = val['idc-name']
        address = val['provinces'] + val['city'] + val['county'] + val['address']
        contact = val['contact']
        phone_num = val['phone']
        email = val['email']
        zipcode = val['zipcode']
        display_addr = val['provinces'] + val['city']
        add_time = base.get_datetime()
        idc = IDCs(idc_name = idc_name,
                   address = address,
                   display_addr = display_addr,
                   contact = contact,
                   phone_num = phone_num,
                   email = email,
                   code = zipcode,
                   add_time = add_time,
                   )
        
        idc.save()
        if idc.id:  
            return HttpResponse(base.dump_json(0), content_type="application/json")
        else:
            return HttpResponse(base.dump_json(1), content_type="application/json")
    else: return HttpResponse("xxx")
    
def list_idc(request):
    idcs = IDCs.objects.all()
    
    return render_to_response('resource.html', {'top_title' : '机房管理', 'idcs' : idcs}, context_instance=RequestContext(request))
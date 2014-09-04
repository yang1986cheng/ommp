#coding: utf-8
import json
import datetime

def get_post_val(request):
    val = {'address' : request.get('address', ''),
           'zipcode' : request.get('zipcode', ''),
           'contact' : request.get('contact', ''),
           'phone' : request.get('phone', ''),
           'email' : request.get('email', ''),
           'idc_name' : request.get('idc-name', ''),
           'provinces' : request.get('provinces', ''),
           'county' : request.get('county', ''),
           'city' : request.get('city', ''),
           'end_date' : request.get('end-date', ''),
           'idc_id' : request.get('idc_id', ''),
           'address' : request.get('address', '')
           }
    return val

def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def dump_json(code):
    if code == 0:
        status = 'success'
    elif code ==1:
        status = 'failed'
    raw_json = {'status': status, 'code' : code,}

    return json.dumps(raw_json)
    
def get_idc_json(obj):
    val = {'id' : obj.id,
           'address' : obj.address,
           'zipcode' : obj.zipcode,
           'contact' : obj.contact,
           'phone' : obj.phone,
           'email' : obj.email,
           'idc-name' : obj.idc_name,
           'provinces' : obj.provinces,
           'county' : obj.county,
           'city' : obj.city,
           }
    
def check_post_val(*args):
    x = True
    for i in args:
        if not i:
            x = False
            break
    return x


















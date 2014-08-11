#coding: utf-8
import json
import datetime

def get_post_val(request):
    val = {'address' : request.get('address', ''),
           'zipcode' : request.get('zipcode', ''),
           'contact' : request.get('contact', ''),
           'phone' : request.get('phone', ''),
           'email' : request.get('email', ''),
           'idc-name' : request.get('idc-name', ''),
           'provinces' : request.get('provinces', ''),
           'county' : request.get('county', ''),
           'city' : request.get('city', ''),
           }
    return val

def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def dump_json(code):
    if code == 0:
        status = 'OK'
    elif code ==1:
        status = 'Failed'
    raw_json = {'status': status, 'code' : code,}
    
    return json.dumps(raw_json)
    
    
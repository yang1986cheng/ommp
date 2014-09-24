#coding: utf-8
import json
import base64, hashlib
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

def get_now_date():
    return datetime.date.today().strftime('%m/%d/%Y')


def sum_page_from_to_end(page, rows):
    page = int(page)
    rows = int(rows)
    page = 1 if page == 0 else page
    r_from = (page - 1) * rows
    r_end = r_from + rows
    
    return [r_from, r_end]

def get_check_code(instr):
    hash = hashlib.md5()
    hash.update(instr.strip())
    return base64.encodestring(hash.digest())











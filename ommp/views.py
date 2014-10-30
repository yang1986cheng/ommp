#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.views.decorators.csrf import csrf_protect
import json

def index(request):
    return render_to_response('test.html')

@login_required
def deploy_index(request):
    if request.method == 'POST':
        return render_to_response('index.html')
    else: return render_to_response('index.html')
    
def welcome(request):
    return render_to_response('welcome.html')

def side(request):
    return render_to_response('side.html')
        
def test(request):
    return HttpResponseRedirect('/management/')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from django.http import HttpResponse, Http404

def listpro(request):
    return render_to_response('project.html', context_instance=RequestContext(request))
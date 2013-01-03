from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def profile(request):
    return render_to_response('registration/profile.html', context_instance=RequestContext(request))
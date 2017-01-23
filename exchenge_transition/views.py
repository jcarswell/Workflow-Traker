from django.shortcuts import render
from djago.http import HttpResponse, Http404
from djago.template import loader

from .models import Users, UserStep

# Create your views here.

def index(request):
    users = Users.objects.order_by('name')
    return HttpResponse(render(request, 'exchange_transition/index.html', { 'users' : users }))

def user(request, username):
    try 
        user = Users.objects.get(name=username)
    except Users.DoesNotExist
        raise Http404("User %s does not exist" % username)

    steps
    context = {
        'user' : user
        'steps' : steps
    }

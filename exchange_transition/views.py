from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpRequest
from django.template import loader

from .models import User, UserStep, Step

# Create your views here.

def index(request):
    users = User.objects.order_by('name')
    return HttpResponse(render(request, 'exchange_transition/index.html', { 'users' : users }))

def user(request, username):
    try:
        user = User.objects.get(name=username)
        steps = UserStep.objects.get(name=username)
    except Users.DoesNotExist:
        raise Http404("User %s does not exist" % username)

    steps
    context = {
        'user' : user,
        'steps' : steps,
        }
    return HttpResponse(render(request, 'exchange_transition', context))

def submit(request, username):
    try:
        user = User.objects.get(name=username)
        try:
            step = user.UserStep_set.get(step=request.POST['stepOrder'])
        except user.UserStep_set.DoesNotExist:
            pass
            # check if step exist or raise 404
    except Users.DoesNotExist:
        raise Http404("User %s does not exist" % username)


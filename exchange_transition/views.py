from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.template import loader
from .models import User, UserStep, Step

# Create your views here.

def index(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            users = User.objects.order_by('name')
            request.session.delete_test_cookie()
            if request.COOKIES.has_key('techname'):
                techname = request.COOKIES['techname']
            else:
                techname = ""
            return HttpResponse(render(request, 'exchange_transition/index.html', { 'users' : users, 'techname' : techname }))
        else:
            return HttpResponse("Cookies are required to use this site, please enable cookies and try again")
    request.session.set_test_cookie()
    return HttpResponse(render(request, 'exchange_transition/index.html'))

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
    if request.method != 'POST':
        return redirect(index)
    if 
    try:
        user = User.objects.get(name=username)
        try:
            step = user.UserStep_set.get(step=request.POST['stepOrder'])
        except user.UserStep_set.DoesNotExist:
            pass
            # check if step exist or raise 404
    except Users.DoesNotExist:
        raise Http404("User %s does not exist" % username)


from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.template import loader
from .models import User, UserStep, Step

# Create your views here.

def index(request):
    users = User.objects.order_by('name')
    if request.COOKIES.has_key('techname'):
        techname = request.COOKIES['techname']
    else:
        techname = ""
    request.session.set_test_cookie()
    context = { 
        'users' : users,
        'techname' : techname,
    }

    return HttpResponse(render(request, 'exchange_transition/index.html', context))

def user(request, username):
    if request.COOKIES.has_key('techname'):
        techname = request.COOKIES['techname']
    else:
        return HttpResponse("Technician name not available, please return to the main page a try again")

    try:
        user = User.objects.get(name=username)
        steps = UserStep.objects.get(name=username)
    except Users.DoesNotExist:
        raise Http404("User %s does not exist" % username)
    request.session.set_test_cookie()

    steps
    context = {
        'user' : user,
        'steps' : steps,
        }
    return HttpResponse(render(request, 'exchange_transition', context))

def submit(request, username):
    if request.method != 'POST':
        return redirect(index)
    else:
        if request.COOKIES.has_key('techname'):
            techname = request.COOKIES['techname']
        else:
            return HttpResponse("Technician name not available, please return to the main page a try again")

        try:
            redirectURL = request.POST['redirect']
        except:
            redirectURL = ''

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return redirect(redirectURL)
        else:
            return HttpResponse("Cookies are required to use this site, please enable cookies and try again")
        try:
            user = User.objects.get(name=username)
            try:
                step = user.UserStep_set.get(step=request.POST['stepOrder'])
            except user.UserStep_set.DoesNotExist:
                raise Http404("Invalid step ID")
            # check if step exist or raise 404
        except Users.DoesNotExist:
            raise Http404("User %s does not exist" % username)


from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.template import loader
from .models import User, UserStep, Step
from .helper import *

# Create your views here.

def index(request):
    users = User.objects.order_by('name')
    techname = str(request.COOKIES.get('techname', ''))
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
    return HttpResponse(render(request, 'exchange_transition/user.html', context))

def submit(request):
    if request.method != 'POST':
        return redirect(index)
    else:
        if 'techname' in request.COOKIES:
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

def manage_root(request):
    if requst.method != 'GET':
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    HttpResponse(render(request, 'exchange_transition/admin.html'))

def manage_view_users(request, userAdded=None):
    if request.method != 'GET': 
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    allUsers = User.objects.order_by('name')
    context = {
        "users" : allUsers,
    }
    return HttpResponse(render(request, 'exchange_transition/admin_view_users.html', context))

def manage_view_steps(request, stepAdded=None):
    if request.method != 'GET': 
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    allSteps = Step.objects.all()
    context = {
        "steps" : allSteps,
    }
    return HttpResponse(render(request, 'exchange_transition/admin_view_steps.html', context))

def manage_report(request, userAlias=None, orderId=None):
    if request.method != 'GET': 
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
    if request.method == 'GET':
        usersteps = UserStep.objects.order_by('user')
        context = {
            "userstep" : userstep,
        }
        return HttpResponse(render(request, 'exchange_transition/admin_report.html', context))

def manage_delete_step(request, orderId):
    if request.metord != 'POST':
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
    
    try:
        step = Step.opbjects.get(order=order)
    except Step.DoesNotExist:
        return HttpResponse("Step with at %s does not exist" % str(order))
    
    name = step.name
    step.delete()
    Step_Helper().reorder()
    return HttpResponse("Step %s. %s was removed successfully" % (str(order), name))

def manage_delete_user(request, userAlias):
    if request.metord != 'POST':
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
    
    try:
        userDel = User.objects.get(alias=userAlias)
    except User.DoesNotExist:
        return HttpResponse("User with alias %s does not exist" % userAlias)
    
    userName = userDel.name
    userDel.delete()
    return HttpResponse("User %s was removed Successfully" % userName)

def manage_new_step(request):
    if request.method == 'POST':
        try:
            order = request.POST['order']
            name = request.POST['name']
            description = request.POST['description']
        except ValueError:
            return HttpResponse("Error All fields are requred")
        else:
            newStep = Step(order=order, name=name, description=description)
            Step_Helper().preSave(order)
            try:
                newStep.save()
            except Exception:
                Step_Helper().reorder() #Make sure we remove the space that was created
                return HttpResponse("error while saving, please contact the web admin for additional details")
            else:
                UserStep_Helper().addStep(order)
        
        return redirect('manage_view_step', stepAdded=True)
            
    elif request.method == 'GET':
        return HttpResponse(render(request, 'excahnge_transition/admin_new_step.html'))
    
    else: 
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
 
def manage_new_user(reqest):
    if request.method == 'POST':
        try:
            userName = requets.POST['name']
            userAlias = request.POST['alias']
        except ValueError:
            return HttpResponse("Error all fields are required")
        else:
            newUser = User(name=userName, alias=userAlias)
            try:
                newUser.save()
            except Exception:
                return HttpResponse("error while saving, please contact the web admin for additional details")
            else:
                UserStep_Helper().addUser(userName)

        return redirect('manage_view_user', userAdded=True)
        
    elif request.method == 'GET':
        return HttpResponse(render(request, 'exchange_transition/admin_new_user.html', context))

    else:
        return HttpResponse(status="405", reason="Request method %s is not allowed" % request.method)

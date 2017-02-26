from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpRequest
from django.template import loader
from .models import User, UserStep, Step
from .helper import *

# Create your views here.

def index(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            return HttpResponse("Cookies are required to use this site")
        if 'techname' in request.COOKIES:
            techname = request.COOKIES['techname']
        elif 'techname' in request.POST:
            try:
                techname = request.POST['techname']
            except ValueError:
                return HttpResponse("Technician name not available, please return to the main page a try again")
        else:
            return HttpResponse("Technician name not available, please return to the main page a try again")

        try:
            useralias = request.POST['useralias']
        except:
            context = { 
                'users' : User.objects.order_by('name'),
                'techname' : techname,
            }
            request.session.set_test_cookie()
            response = HttpResponse(render(request, 'exchange_transition/index.html', context))
            response.set_cookie('techname', techname)
            return response
        else:
            return redirect(reverse('et_user', kwargs={'userAlias' : useralias}))
    elif request.method == 'GET':
        try:
            techname = request.COOKIES['techname']
        except:
            request.session.set_test_cookie()
            return HttpResponse(render(request, 'exchange_transition/index.html'))

        request.session.set_test_cookie()
        context = { 
            'users' : User.objects.order_by('name'),
            'techname' : techname,
        }
        request.session.set_test_cookie()
        return HttpResponse(render(request, 'exchange_transition/index.html', context))
    else:
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)


def user(request, userAlias):
    if 'techname' in request.COOKIES:
        techname = request.COOKIES['techname']
    else:
        return HttpResponse("Technician name not available, please return to the main page a try again")

    try:
        user = User.objects.get(alias=userAlias)
    except Users.DoesNotExist:
        raise Http404("User %s does not exist" % userAlias)
    request.session.set_test_cookie()

    context = {
        'user' : user,
        'steps' : Step.objects.order_by('order'),
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
    if request.method != 'GET':
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    return HttpResponse(render(request, 'exchange_transition/admin.html'))

def manage_view_users(request, userAdded=None):
    if request.method != 'GET': 
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    context = {
        "users" : User.objects.order_by('name'),
    }
    return HttpResponse(render(request, 'exchange_transition/admin_view_users.html', context))

def manage_view_steps(request, stepAdded=None):
    if request.method != 'GET': 
        raise HttpResponse(status="405", reason="request method %s is not allowed" % request.method)

    context = {
        "steps" : Step.objects.order_by('order'),
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

def manage_new_step(request):
    if request.method == 'POST':
        try:
            order = int(request.POST['order'])
            name = request.POST['name']
            description = request.POST['description']
            try:
                returnAction = request.POST['submit']
            except:
                returnAction = "Save"
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
        if returnAction == "Save":
            return redirect(reverse('et_manage_view_steps'))
        else:
            context = {
                "stepcount" : range(1, Step.objects.order_by('-order')[0].order + 2),
                "added" : True,
            }
            return HttpResponse(render(request, 'exchange_transition/admin_new_step.html', context))

            
    elif request.method == 'GET':
        try:
            lastStepOrder = Step.objects.order_by('-order')[0].order
        except:
            lastStepOrder = 0

        context = {
            "stepcount" : range(1, lastStepOrder + 2),
        }
        return HttpResponse(render(request, 'exchange_transition/admin_new_step.html', context))
    
    else: 
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
 
def manage_new_user(request):
    if request.method == 'POST':
        try:
            userName = request.POST['name']
            userAlias = request.POST['alias']
            userComments = request.POST['comments']
            try:
                returnAction = request.POST['submit']
            except:
                returnAction = "Save"
        except ValueError:
            return HttpResponse("Error all fields are required")
        else:
            newUser = User(name=userName, alias=userAlias, comments=userComments)
            try:
                newUser.save()
            except Exception:
                return HttpResponse("error while saving, please contact the web admin for additional details")
            else:
                UserStep_Helper().addUser(userAlias)
        
        if returnAction == "Save":
            return redirect(reverse('et_manage_view_user'))
        else:
            return HttpResponse(render(request, 'exchange_transition/admin_new_user.html', {"added" : True}))
        
    elif request.method == 'GET':
        return HttpResponse(render(request, 'exchange_transition/admin_new_user.html'))

    else:
        return HttpResponse(status="405", reason="Request method %s is not allowed" % request.method)

def manage_user(request, userAlias):
    try:
        currentUser = User.objects.get(alias=userAlias)
    except:
        raise Http404("Error: User not found")
    
    if request.method == 'POST':
        try:
            userName = request.POST['name']
            userAlias = request.POST['alias']
            try:
                returnAction = request.POST['submit']
            except:
                returnAction = "Save"
        except ValueError:
            return HttpResponse("Error all fields are required")
        if returnAction == "Save":
            currentUser.name = userName
            currentUser.alias = userAlias
            currentUser.save()
            return redirect(reverse('et_manage_view_users'))
        elif returnAction == "Delete":
            currentUser.delete()
            return redirect(reverse('et_manage_view_users'))
        else:
            return redirect(reverse('et_manage_view_users'))

    elif request.method == 'GET':
        if currentUser.completed:
            completed = "Yes"
        else:
            completed = "%s/%s" % (UserStep.objects.filter(user=currentUser).filter(completed=True).count(),
                UserStep.objects.filter(user=currentUser).count())
        context = {
            "name" : currentUser.name,
            "alias" : currentUser.alias,
            "completed" : completed,
            "completedBy" : currentUser.completedBy,
            "comments" : currentUser.comments,
        }
        return HttpResponse(render(request, 'exchange_transition/admin_user.html', context))

    else:
        return HttpResponse(status="405", reason="Request method %s is not allowed" % request.method)

def manage_step(request, orderId):
    try:
        currentStep = Step.objects.get(order=orderId)
    except:
        raise Http404("Error: Step does not exist")
    if request.method == 'POST':
        try:
            name = request.POST['name']
            description = request.POST['description']
            try:
                returnAction = request.POST['submit']
            except:
                returnAction = "Save"
        except:
            pass
        if returnAction == "Save":
            currentStep.name = name
            currentStep.description = description
            currentStep.save()
            return redirect('et_manage_view_steps')
        elif returnAction == "Delete":
            currentStep.delete()
            Step_Helper().reorder()
            return redirect('et_manage_view_steps')
        else:
            return redirect('et_manage_view_steps')
            
    elif request.method == 'GET':
        context = {
            "order" : currentStep.order,
            "description" : currentStep.description,
            "name" : currentStep.name,
            "completed" : "%s/%s" % (UserStep.objects.filter(step=currentStep).filter(completed=True).count(),
                UserStep.objects.filter(step=currentStep).count()),
        }
        return HttpResponse(render(request, 'exchange_transition/admin_step.html', context))
    
    else: 
        return HttpResponse(status="405", reason="request method %s is not allowed" % request.method)
 

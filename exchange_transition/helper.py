from .models import User, Step, UserStep
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UserStep_Helper():
    def addUser(self, userName):
        """ 
        This function is used to create the UserStep objects
        when a new user is created, it will be called from the
        handlers file as post_save signel handler

        This function take the created User objects name as the
        only argument and returns nothing

        This function will raise a vaildation error if the user
        does not exist
        """
        try:
            userAdd User.objects.get(name = userName)
        except User.DoesNotExist:
            raise ValidationError( { "User" : _("Invalid User received") } )

        stepAll = Step.objects.all()
        for stepX in stepAll:
            new = UserStep(user=userAdd,step=stepX)
            new.save()
            new = None

        stepAll = None

    def addStep(self, stepOrder):
        """ 
        This function is used to create the UserStep objects
        when a new step is added, it will be called from the
        handlers file as post_save signel handler

        This function takes the created Step objects order as the
        only argument and returns nothing

        This function will raise a vaildation error if the Step
        does not exist
        """
        try:
            stepNew = Step.objects.get(order=stepOrder)
        except Step.DoesNotExist:
            raise ValidationError( { "Step" : _("Invalid Step received") } )
            
        userAll = User.objects.all()
        for userX in userAll:
            new = UserStep(user=userX, step=stepNew)
            new.save()
            new = None

        userAll = None

class Step_Helper():
    def reorder(self):
        stepLast = Step.objects.order_by('-order')[1]
        orderLast = stepLast.order
        orderX = 0
        if orderLast == Step.objects.count():
            return #No need to go further as the higest order value is equal to the total number of objects

        for stepX in range(1,orderLast+1)
            try:
                stepCur = Step.objects.get(filter=stepX)
            except Step.DoesNotExist:
                pass #We will find the next valid object and set the order to orderX+1
            else:
                if stepCur.order != (orderX + 1): #if the object is out of order correct it
                    orderX += 1
                    stepCur.order = orderX
                    stepCur.save()
                else: #Otherwise just increment orderX
                    orderX += 1
        
    def preSave(self, orderAdd):
        if orderAdd <= Step.objects.order_by('-order')[1].order:
            #Don't put the following in a for loop as it will be recursive on object save
            try:
                stepCur = Step.objects.get(order=orderAdd)
            except Step.DoesNotExist:
                self.reorder() #call the reorder function incase theres a gap and try again
                try:
                    stepCur = Step.objects.get(order=stepX)
                except Step.DoesNotExist:
                    raise Exception("Somethings gone wrong it seems that there no steps")
 
            stepCur.order += 1
            stepCur.save() #this will trigger pre_save again ang recuse until the order has been updated
            stepCur = None

    def postDelete(self):
        self.reorder() #Just for cleanliness sake


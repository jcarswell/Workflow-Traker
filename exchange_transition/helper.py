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
            userAdd = User.objects.get(name = userName)
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
        """
        reorder is a helper function for the Step model. It is used
        to ensure that all of the Step Orders are in line and are without
        incongruity. this function should be used sparingly and only when
        there are no duplicates in the database. if this function is called
        and there is duplicates it could cause all of the objects beyond
        the duplicate to be thrown way out of order.
        
        Arguements:
            None 
        """
        if Step.objects.count() < Step.objects.order_by('-order')[0].order:
            stepOrderLast = Step.objects.order_by('-order')[0].order
        else:
            stepOrderLast = Step.objects.count()
        
        orderX = stepOrderCurrent = 1
        while stepOrderCurrent <= stepOrderLast:
            try:
                stepCurrent = Step.objects.get(order=stepOrderCurrent)
            except Step.DoesNotExist:
                pass #We will find the next valid object and set the order to orderX+1
            except Step.MultipleObjectsReturned:
                #We will cause this exception to be encounter until all objects have a unique ID
                # alternatively an admin would have to login and correct the issue manually or
                # from the admin site. We will only increment the last step by one. Though this
                # may be dangerous as it could cause a Step to go from its correct postition to
                # the last step.
                for stepCurrent in Step.objects.filter(order=stepOrderCurrent)[1:]:
                    stepCurrent.order += 1
                    stepCurrent.save()
                    
                stepCurrent = None
            else:
                if stepCurrent.order != (orderX): #if the object is out of order correct it
                    stepCurrent.order = orderX
                    stepCurrent.save()
                    stepCurrent = None
                    orderX += 1
                else: #Otherwise just increment orderX
                    orderX += 1

            stepOrderCurrent += 1
        
    def preSave(self, orderAdd):
        """
        preSave is a helper function that ensure that before 
        a new object is added that the orders are correct and 
        that argument orderAdd is not going to overlap with an
        existing order. 
        
        Arguments:
            self        : the class must be initialized 
            orderAdd    : take an integer and is the order ID
                that a new Step is to be saved
        """
        stepOrderCurrent = Step.objects.order_by('-order')[1].order
        while stepOrderCurrent >= orderAdd:
            try:
                print("retriving step %i" % stepOrderCurrent)
                stepCurrent = Step.objects.get(order=stepOrderCurrent)
            except Step.DoesNotExist:
                self.reorder() #call the reorder function incase theres a gap and try again
                try:
                    stepCurrent = Step.objects.get(order=stepOrderCurrent)
                except Step.DoesNotExist:
                    raise Exception("Somethings gone wrong it seems that there no steps")
 
            stepCurrent.order += 1
            stepCurrent.save() 
            stepCurrent = None

            stepOrderCurrent -= 1


    def postDelete(self):
        self.reorder() #Just for cleanliness sake


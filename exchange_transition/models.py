from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from re import compile as re

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    alias = models.CharField(max_length=100, null=True)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField(null=True)
    completedBy = models.CharField(max_length=200, null=True)
    comments = models.TextField(default="** Enter Relevent notes here **")

    def __str__(self):
       return self.name

    def clean(self):
        validChar = re("^[a-zA-Z0-9\-_\.]{1,99}$")
        if (self.alias == None or self.alias == ""):
            raise ValidationError( {"alias" : _("Alias may not be empty")} )
        if validChar.match(self.alias) is None:
            raise ValidationError( {"alias" : _("Alias contains invalid characters")} )
        

class Step(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return "%i. %s" % (self.order, self.name)

    def save(self):
        try:
            Step.objects.get(order=self.order)
            n = int(Step.Objects[-1].order) * -1 # convert n to negative so we can count backwards and don't violate ordering
            for x in range(n, ((int(self.order) - 1) * -1)): # for x in range(-1,0) will produce one iteration of -1
                x *= -1 # convert x to a positive and process order update
                fUpdate = Step.objects.get(order=x)
                fUpdate.order = x + 1 # order = i
                fUpdate.save()

        except Step.DoesNotExist:
            pass # We don't need to do anything if the order is already unique

        super(Step, self).save()

        #create UserStep objects

    def delete(self):
        delorder = self.order
        super(Step, self).delete()
        n = int(Step.objects[-1].order)
        if n > order:
            for x in range(order + 1, n + 1): # Close the order gap
                fUpdate = Step.objects.get(order=x)
                fUpdate.order = x - 1 # order = i
                fUpdate.save()

class UserStep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField()
    unique_together = ("user","step")


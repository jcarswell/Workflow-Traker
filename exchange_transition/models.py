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
    completedBy = models.CharField(max_length=200, null=True, blank=True)
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

class UserStep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField()
    completedBy = models.CharField(max_length=200, blank=True, null=True)
    unique_together = ("user","step")
    

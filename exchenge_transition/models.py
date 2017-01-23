from django.db import models
from django.core.validators import validate_email

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=200, unique=True)
    emailaddress = models.CharField(max_length=255, validators=[validate_email])
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField(null=True)

    def __str__(self):
       return name


class Steps(models.Model):
    order = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)

class UserStep(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    step = models.ForeignKey(Steps, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField()
    unique_together = ("user","step")


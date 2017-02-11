from django.core import signals
from django.dispatch import receive
from .helper import UserStep_Helper, Step_Helper
from .models import User, Step

@receive(pre_save, sender=Step)
def step_pre_save(sender, **kwargs):
    Step_Helper.preSave(kwargs['order'])

@receive(post_save, sender=Step)
def step_post_save(sender, **kwargs):
    UserStep_Helper.AddStep(kwargs['order'])

@receive(post_delete, sender=Step)
def step_post_delete(sender, **kwargs):
    Step_Helper.postDelete()

@receive(post_save, sender=User)
def user_post_save(sender, **kwargs):
    UserStep_Helper.AddUser(kwargs['name'])


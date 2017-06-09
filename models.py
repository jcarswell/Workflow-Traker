from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from re import compile as re

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    alias = models.CharField(max_length=100, null=True, unique=True)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField(null=True)
    completedBy = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField(null=True)

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
    optional = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return "%i. %s" % (self.order, self.name)

class UserStep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completedOn = models.DateTimeField(null=True)
    completedBy = models.CharField(max_length=200, blank=True, null=True)
    unique_together = ("user","step")
    
class ConfigLdap(models.Model):
    dc = models.CharField(max_length=255, null=False, unique=True)
    user = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    search = models.CharField(max_length=255)
    tls = models.BooleanField(default=False)
    tls_untrusted = models.BooleanField(default=False)
    server = models.models.CharField(max_length=255)
    port = models.IntegerField(default=389)

    def __str__(self):
        return "%s (%s)" % (seld.server, self.dc)

class ConfigGroupPriv(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    priv_admin = models.BooleanField(default=False)      #grants full access to everything
    priv_pj_admin = models.BooleanField(default=False)   #grants administer all projects
    priv_pj_manager = models.BooleanField(default=False) #grants pivilege to manage owned projects
    priv_user = models.BooleanField(default=False)       #grants access to work on assigned projects and tasks

    def __str__(self):
        return self.name

class ConfigLdapMap(models.Model):
    local_group = models.ForeignKey(ConfigGroupPriv.name, on_delete=models.CASCADE)
    ldap = models.ForeignKey(ConfigLdap, on_delete=models.CASCADE)
    ldap_cn = models.CharField(max_length=255, null=False)
    ldap_type = models.CharField(max_length=255)

    def __str__(self):
        return self.ldap_cn

class ConfigUser(models.Model):
    user = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    pw_last_set - models.DateTimeField(auto_now_add=True, blank=True)
    group = models.ForeignKey(ConfigGroupPriv.name, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ConfigUserPasswd(model.Model):
    """
    This model is for storing the users privious x passwords
    ensuring that this is update/cleaned up on update is implemeted
    in software
    """
    
    user = models.ForeignKey(ConfigUser.user, on_delete=models.CASCADE)
    passwd = models.CharField(max_length=64, null=False)
    salt = models.CharField(max_length=64, null=False)
    current = models.BooleanField(default=True)

    unique_together = ((user,passwd),)

from django.contrib import admin
from django import forms
from .models import User,Step

class UsersAdmin(admin.ModelAdmin):
    class Meta:
        model = User

    readonly_fields = ('completedOn', 'comments')
    seach_fields = ('name', 'emailaddress')
    ordering = ('-completed', 'name')
    list_display = ('completed', 'name', 'alias', 'completedOn')
    list_filter = ['completed']

    fieldsets = (
        (None, { 'fields' : ('name', 'alias', 'completedOn', 'comments') }),
        ('Admin Options', {
            'classes': ('collapse' ,),
            'fields' : ('completed', 'completedBy'),
        }),
        )

class StepsAdmin(admin.ModelAdmin):
    class Meta:
        model = Step

    search_fields = ['name']
    ordering = ['order']
    list_display = ('order', 'name', 'description')
    list_filter = []

admin.site.register(User, UsersAdmin)
admin.site.register(Step, StepsAdmin)

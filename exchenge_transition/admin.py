from django.contrib import admin

from .models import Users,Steps

class UsersAdmin(admin.ModelAdmin):
    class Meta:
        model = Users

    seach_fields = ('name', 'emailaddress')
    ordering = ('-completed', 'name')
    list_display = ('completed', 'name', 'emailaddress', 'completedOn')
    list_filter = ['completed']

class StepsAdmin(admin.ModelAdmin):
    class Meta:
        model = Steps

    search_fields = ['name']
    ordering = ['order']
    list_display = ('order', 'name', 'description')
    list_filter = []

admin.site.register(Users, UsersAdmin)
admin.site.register(Steps, StepsAdmin)

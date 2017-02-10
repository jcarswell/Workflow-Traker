from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='et_index'),
    url(r'^(?P<user_alias>[a-zA-Z0-9\-_.]+)/$', views.user, name='et_user'),
    url(r'^(?P<user_alias>[a-zA-Z0-9\-_.]+)/submit/$', views.submit, name='et_submit'),
    ]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='et_index'),
    url(r'^u/(?P<userAlias>[a-zA-Z0-9\-_.]+)/$', views.user, name='et_user'),
    url(r'^Manage/$', views.manage_root, name='et_manage'),
    url(r'^Manage/users/$', views.manage_view_users, name='et_manage_view_users'),
    url(r'^Manage/steps/$', views.manage_view_steps, name='et_manage_view_steps'),
    url(r'^Manage/report/$', views.manage_report, name='et_manage_report'),
    url(r'^Manage/report/(?P<userAlias>[a-zA-Z0-9\-_.]+)/$', views.manage_report_user, name='et_manage_report_user'),
    url(r'^Manage/user/$', views.manage_new_user, name='et_manage_new_user'),
    url(r'^Manage/step/$', views.manage_new_step, name='et_manage_new_step'),
    url(r'^Manage/user/(?P<userAlias>[a-zA-Z0-9\-_.]+)/$', views.manage_user, name='et_manage_user'),
    url(r'^Manage/step/(?P<orderId>[0-9]{1,4})/$', views.manage_step, name='et_manage_step'),
    ]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='et_index'),
    url(r'u/^(?P<user_alias>[a-zA-Z0-9\-_.]+)/$', views.user, name='et_user'),
    url(r'u/^(?P<user_alias>[a-zA-Z0-9\-_.]+)/submit/$', views.submit, name='et_submit'),
    url(r'^Manage/$', views.manage_root, name='et_manage'),
    url(r'^Manage/users/$', views.manage_view_users, name='et_manage_view_users'),
    url(r'^Manage/steps/$', views.manage_view_steps, name='et_manage_view_steps'),
    url(r'^Manage/report/$', views.manage_report, name='et_manage_report'),
    url(r'^Manage/user/$', views.manage_new_user, name='et_manage_new_user'),
    url(r'^Manage/step/$', views.manage_new_step, name='et_manage_new_step'),
    url(r'^Manage/user/(?P<userAlias>[a-zA-Z0-9\-_.]+)/$', views.manage_report, name='et_manage_report_user'),
    url(r'^Manage/user/(?P<userAlias>[a-zA-Z0-9\-_.]+)/delete/$', views.manage_delete_user, name='et_manage_delete_user'),
    url(r'^Manage/step/(?P<orderId>[0-9]{1,4})/$', views.manage_report, name='et_manage_report_step'),
    url(r'^Manage/step/(?P<order_id>[0-9]{1,4})/delete/$', views.manage_delete_step, name='et_manage_delete_step'),
    ]

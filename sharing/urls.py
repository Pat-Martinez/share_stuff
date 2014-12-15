# ****** Sharing URLS.py ***********

from django.conf.urls import patterns, url
from sharing import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?i)about/$', views.about, name='about'),
        url(r'^(?i)register/$', views.register, name='register'),
        url(r'^(?i)sign_in/$', views.sign_in, name='sign_in'),
        url(r'^(?i)add_item/$', views.add_item, name='add_item'),
        url(r'^(?i)inventory/item_info/(?P<item_id>\w+)/$', 
                views.item_info, name='item_info'),
        url(r'^(?i)add_group/$', views.add_group, name='add_group'),
        url(r'^(?i)sign_out/$', views.sign_out, name='sign_out'),
        url(r'^(?i)inventory/$', views.inventory, name='inventory'),
        url(r'^(?i)join_requests/$', views.join_requests, name='join_requests'),
        url(r'^(?i)join_requests/process/(?P<request_id>\w+)/$', 
                views.join_req_process, name='process'),
        url(r'^(?i)inventory/delete_item/(?P<item_id>\w+)/$', 
                views.delete_item, name='delete_item'),
        url(r'^(?i)groups/$', views.groups, name='groups'),
        url(r'^(?i)groups/group_info/(?P<group_id>\w+)/$', 
                views.group_info, name='group_info'),
        url(r'^(?i)borrow_requests/$', views.borrow_requests, name='borrow_requests'),
        url(r'^(?i)borrow_requests/process/(?P<borrow_id>\w+)/$', 
                views.borrow_req_process, name='process'),
        url(r'^(?i)under_construction/$', views.under_construction, name='under_construction'),
        url(r'^(?i)behind_the_scenes/$', views.behind_the_scenes, name='behind_the_scenes'),


)
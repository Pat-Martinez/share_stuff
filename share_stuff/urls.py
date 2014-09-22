# *******Share_Stuff Project urls.py********

from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sharing/', include('sharing.urls')),
    url(r'^messages/', include('django_messages.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
	    'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}), )


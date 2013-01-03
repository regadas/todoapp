from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    (r'^accounts/', include('accounts.urls')),
    url(r'^', include('cal.urls')),
) + staticfiles_urlpatterns()

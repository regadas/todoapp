from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('',
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^profile/$', 'accounts.views.profile', name='profile'),
    (r'^', include('registration.backends.default.urls')),
)

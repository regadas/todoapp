from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from handlers import TodoHandler, ShareCalendarHandler

urlpatterns = patterns('cal.views',
    url(r'^$', 'index', name="index"),
    url(r'^public/(?P<id>[^/]+)/$', 'public', name="public"),
    url(r'^share/(?P<id>[^/]+)/$', 'share', name="share"),
    url(r'^unshare/(?P<id>[^/]+)/$', 'unshare', name="unshare"),

    url(r'^todos/?$', 'todos', name="todo.list"),
    url(r'^todos/create/?$', 'todos', name="todo.add"),
    url(r'^todos/edit/?$', 'todos', name="todo.edit"),
    url(r'^todos/delete/?$', 'delete', name="todo.delete"),

    # API handlers
    url(r'^api/todos/?$', Resource(TodoHandler)),
    url(r'^api/calendar/public/?$', Resource(ShareCalendarHandler)),
)
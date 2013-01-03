from piston.handler import BaseHandler
from piston.utils import rc
from django.core.urlresolvers import reverse
from models import Calendar, Todo
from accounts.models import UserProfile
from utils import json_response
import json
import settings
import dateutil.parser


#TODO: make this one a decorator
def is_authenticated(request):
    print request.META
    auth_header = 'HTTP_%s' % getattr(settings, 'AUTH_HEADER')
    upper_auth_header = auth_header.upper().replace('-', '_')
    print auth_header
    print upper_auth_header
    auth_string = request.META.get(upper_auth_header, request.META.get(auth_header))
    print auth_string
    return UserProfile.objects.get(api_key=auth_string)


def get_calendar(profile, calendar_id):
    if calendar_id:
        calendar = Calendar.objects.get(id=calendar_id)
        if not calendar.public:
            raise Exception
    else:
        calendar = profile.calendar
    return calendar


class ShareCalendarHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')

    def read(self, request):
        try:
            profile = is_authenticated(request)
            calendar = profile.calendar
            result = {'link': reverse('public', args=[calendar.id])} if calendar.public else {}
            return json_response(result)
        except Exception:
            return rc.FORBIDDEN

    def update(self, request):
        try:
            profile = is_authenticated(request)
            calendar = profile.calendar
            calendar.public = True
            calendar.save()
            return json_response(calendar.to_hash())
        except Exception:
            return rc.FORBIDDEN

    def delete(self, request):
        try:
            profile = is_authenticated(request)
            calendar = profile.calendar
            calendar.public = False
            calendar.save()
            return json_response(calendar.to_hash())
        except Exception:
            return rc.FORBIDDEN


class TodoHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def read(self, request):

        try:
            profile = is_authenticated(request)
            calendar = get_calendar(profile, request.GET.get('calendar', None))

            todos = Todo.objects.filter(calendar=calendar)
            result = {'todos': [todo.to_hash(ignore_cal=True) for todo in todos]}
            return json_response(result)
        except Exception:
            return rc.FORBIDDEN

    def create(self, request):
        try:
            profile = is_authenticated(request)
            calendar = get_calendar(profile, request.GET.get('calendar', None))
            result = json.loads(request.raw_post_data)
            start = dateutil.parser.parse(result['start'])
            end = dateutil.parser.parse(result['end'])
            todo = Todo.objects.create(title=result['title'], start=start, end=end,
                calendar=calendar)
            print todo
            return json_response(todo.to_hash())
        except Exception:
            return rc.FORBIDDEN

    def update(self, request):
        try:
            profile = is_authenticated(request)
            calendar = get_calendar(profile, request.GET.get('calendar', None))

            result = json.loads(request.raw_post_data)

            todo_id = result.get('id', None)
            start = dateutil.parser.parse(result['start'])
            end = dateutil.parser.parse(result['end'])
            Todo.objects.filter(id=todo_id).update(title=result.get('title'),
                start=start, end=end, calendar=calendar)
            todo = Todo.objects.get(id=todo_id)
            return json_response(todo.to_hash())
        except Exception:
            return rc.FORBIDDEN

    def delete(self, request):
        try:
            profile = is_authenticated(request)
            calendar = get_calendar(profile, request.GET.get('calendar', None))

            result = json.loads(request.raw_post_data)
            todo = Todo.objects.get(id=result['id'], calendar=calendar)
            todo.delete()
            return json_response(todo.to_hash())
        except Exception:
            return rc.FORBIDDEN

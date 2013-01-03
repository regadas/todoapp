import json
import logging
import dateutil.parser

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Calendar, Todo
from accounts.models import UserProfile

logger = logging.getLogger(__name__)


def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))


@login_required
def public(request, id):
    if request.method == 'GET':
        try:
            cal = Calendar.objects.get(id=id, public=True)
            owner = UserProfile.objects.get(calendar=cal).user
            return render_to_response('public_index.html', {'owner': owner}, context_instance=RequestContext(request))
        except Exception:
            # BAD request ... calendar is not public we should render a template for this
            return HttpResponse('Calendar not public')


@login_required
def share(request, id):
    if request.method == 'POST':
        cal = Calendar.objects.get(id=id)
        cal.public = True
        cal.save()
        return HttpResponse(json.dumps(cal.to_hash()), content_type='application/json')


@login_required
def unshare(request, id):
    if request.method == 'POST':
        cal = Calendar.objects.get(id=id)
        cal.public = False
        cal.save()
        return HttpResponse(json.dumps(cal.to_hash()), content_type='application/json')


@login_required
def todos(request):
    user_calendar = request.user.get_profile().calendar
    if request.method == 'POST':
        #TODO: test JSON
        result = json.loads(request.raw_post_data)

        calendar_id = result.get('calendar', user_calendar.id)
        current_calendar = Calendar.objects.get(id=calendar_id)
        id = result.get('id', None)
        start = dateutil.parser.parse(result['start'])
        end = dateutil.parser.parse(result['end'])

        if id:
            Todo.objects.filter(id=id).update(title=result.get('title'),
                start=start, end=end, calendar=current_calendar)
            todo = Todo.objects.get(id=id)
        else:
            todo = Todo.objects.create(title=result['title'], start=start, end=end,
                calendar=current_calendar)

        return HttpResponse(json.dumps(todo.to_hash()), content_type='application/json')
    else:
        try:
            calendar_id = request.GET.get('calendar')
            current_calendar = Calendar.objects.get(id=calendar_id)
        except Exception:
            current_calendar = user_calendar
        todos = [todo.to_hash(ignore_cal=True) for todo in Todo.objects.filter(calendar__id=current_calendar.id)]
        return HttpResponse(json.dumps(todos), content_type='application/json')


@login_required
def delete(request):
    result = json.loads(request.raw_post_data)
    todo = Todo.objects.get(id=result['id'])
    todo.delete()
    return HttpResponse(json.dumps(todo.to_hash()), content_type='application/json')





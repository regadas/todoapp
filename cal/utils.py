from django.http import HttpResponse
import json


def json_response(obj, *args, **fields):
    return HttpResponse(json.dumps(obj), content_type='application/json')

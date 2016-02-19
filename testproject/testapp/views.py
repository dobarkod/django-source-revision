import json
from django.template import Template, RequestContext
from django.http import HttpResponse


def return_revision(request):
    return HttpResponse(request.source_revision, content_type='text/plain')


def empty_response(request):
    return HttpResponse('')


def use_context(request):
    tpl = Template(u'{{ SOURCE_REVISION }}')
    ctx = RequestContext(request)
    return HttpResponse(tpl.render(ctx), content_type='text/plain')


def use_staticfiles(request):
    tpl = Template(u"{% load staticfiles %}{% static 'foo' %}")
    ctx = RequestContext(request)
    return HttpResponse(tpl.render(ctx), content_type='text/plain')

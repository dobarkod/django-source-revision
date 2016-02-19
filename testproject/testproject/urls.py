from django.conf.urls import url, include
from django import VERSION

from testapp.views import (return_revision, empty_response, use_context,
    use_staticfiles)


if VERSION >= (1, 9):
    def patterns(prefix, *args):
        return args
else:
    from django.conf.urls import patterns


urlpatterns = patterns('testapp.views',
    url(r'^request$', return_revision),
    url(r'^header$', empty_response),
    url(r'^context$', use_context),
    url(r'^staticfiles$', use_staticfiles),
)

from django.conf import settings
from .loader import get_revision

__all__ = ['get_revision']


class RevisionMiddleware(object):

    def __init__(self):
        self.header = getattr(settings, 'SOURCE_REVISION_HEADER',
            'X-Source-Revision')

    def process_request(self, request):
        request.source_revision = get_revision()

    def process_response(self, request, response):
        rev = get_revision()
        if rev:
            response[self.header] = rev
        return response

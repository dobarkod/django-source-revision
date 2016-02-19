from .loader import get_revision

__all__ = ['source_revision']


def source_revision(request):
    return {u'SOURCE_REVISION': get_revision()}

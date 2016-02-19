from subprocess import check_output, CalledProcessError
from django.conf import settings

__all__ = ['get_revision']

_revision_loaded = False
_revision = None


def get_revision():
    global _revision, _revision_loaded

    if _revision_loaded:
        return _revision

    commands = getattr(settings, 'SOURCE_REVISION_COMMANDS', [
        'git rev-parse --short HEAD',
        'hg id -i'
    ])

    def get_rev():
        for command in commands:
            try:
                rev = check_output(command.split(u' ')).decode('ascii').strip()
            except (CalledProcessError, OSError):
                continue
            if rev:
                return rev
        return None

    _revision = get_rev()
    _revision_loaded = True
    return _revision

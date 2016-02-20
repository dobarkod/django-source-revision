# Django Source Revision

[![Build Status](https://travis-ci.org/dobarkod/django-source-revision.svg?branch=master)](https://travis-ci.org/dobarkod/django-source-revision?branch=master)

A set of utilities for getting and using information about the current
revision (version) of the code being run. Supports git and mercurial out
of the box, other VCS systems can be easily added.

Works with Django (1.4, 1.5, 1.6, 1.7, 1.8, 1.9) and Python (2.6, 2.7, 3.3,
3.4, 3.5).

## Installation

Install from the Python Package Index:

    pip install django-source-revision

## Usage

### Middleware

A Django middleware class is provided to add the revision information to
every incoming request and attach it as header to every response.

To use the middleware, add it to your Django settings:

    MIDDLEWARE_CLASSES += (
        'sourcerevision.middleware.RevisionMiddleware',
    )

If revision information is available, the `django.http.HttpRequest` object
passed to your view functions will contain an extra `source_revision`
attribute:

    def myview(request):
        print "running code at version", request.source_revision

The revision information, if available, will also be added to the response
headers. By default, `X-Source-Revision` header will be set. Header name can
be customized using the `SOURCE_REVISION_HEADER` setting.

### Context processor

A context processor is provided which adds `SOURCE_REVISION` variable to
the request context. To use, add the processor to your list of context
processors:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'context_processors': [
                    'sourcerevision.context_processors.source_revision'
                ]
            },
            ...
        }

(if you're using Django version older than 1.9, you'll need to modify
`TEMPLATE_CONTEXT_PROCESSORS` setting instead).

### Drop-in staticfiles replacement

A drop-in staticfiles replacement is provided which automatically adds
revision suffix to all static assets, thereby providing static asset
versioning. This means that whenever your code changes, the URLs of static
assets will change as well, forcing the browsers to re-request the assets.

To enable this, add `sourcerevision` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS += ('sourcerevision,')

After this, you can load the `staticfiles` template library and use the
`static` tag in your templates as usual:

    {% load staticfiles %}
    <script src="{% static 'script.js' %}"></script>

Note: the replacement tag doesn't provide the variant to save the static file
URL to a variable, ie. this will not work (while it would with original
`staticfiles`):

    {% static 'script.js' as script_url %}

### Manual use

If your use case is not covered by the helpers described above, you can
get the revision directly:

    from sourcerevision.loader import get_revision
    print get_revision()

### Customizing VCS revision checks

Out of the box, sourcevision supports git and mercurial. To add support to
another VCS system, you need to provide a command to execute that will return
(only) the revision number (git commit id, changeset id for mercurial, etc).

More than one command can be provided, and they will be tried in the order
specified. The default commands are:

    SOURCE_REVISION_COMMANDS = [
        'git rev-parse --short HEAD', # for git
        'hg id -i' # for mercurial
    ]

If you add support for additional VCS systems (such as subversion, darcs
or others), please consider contributing it to this project (see below for
guidelines for contributors).

## Testing

To run tests, use the `tox` command (https://pypi.python.org/pypi/tox)

    tox  # for all supported python and django versions

If you need you can run tox just for single environment:

    tox -e py27_django17

For available test environments refer to `tox.ini` file.

## Contributing

Pull requests are welcome! Before adding a new feature, check with the
maintainers (via the issue tracker) if it fits within the architecture and
the scope of the package. Before making the PR, check that your code
conforms to the Python coding style (PEP-8), has complete test coverage, and
passes all the tests.

## License

Copyright (C) 2016. Good Code and Django Source Revision contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

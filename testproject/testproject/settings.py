# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import sys
sys.path.insert(0, os.path.dirname(BASE_DIR))

from django import VERSION

SECRET_KEY = 'm!qp4^7#f*87&l2r7tr2qx2_@sabi6pf87b=3sdbt3b8b3hw$y'
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'testapp',
)

if VERSION >= (1, 8):
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'context_processors': [
                    'sourcerevision.context_processors.source_revision'
                ]
            }
        }
    ]
else:
    TEMPLATE_CONTEXT_PROCESSORS = [
        'sourcerevision.context_processors.source_revision'
    ]

MIDDLEWARE_CLASSES = [
    'sourcerevision.middleware.RevisionMiddleware'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'testproject.urls'
WSGI_APPLICATION = 'testproject.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

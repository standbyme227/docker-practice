from .base import *

DEBUG = True

secrets = json.loads(open(SECRETS_DEV, 'rt').read())

ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.production.application'

INSTALLED_APPS += [
    'django_extensions',
]

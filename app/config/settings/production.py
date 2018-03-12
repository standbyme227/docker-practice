from .base import *

DEBUG = True

secrets = json.loads(open(SECRETS_PRODUCTION, 'rt').read())

ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.production.application'

INSTALLED_APPS += [
    'django_extensions',
]


DEFAULT_FILE_STORAGE = 'config.storage.DeFaultFilesStorage'
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'
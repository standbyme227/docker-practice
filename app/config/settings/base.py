"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import importlib
import json
import numbers
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import raven

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# app 폴더가 Base 파란색 폴더

ROOT_DIR = os.path.dirname(BASE_DIR)
# docker-prac가 Root

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS_BASE = os.path.join(SECRETS_DIR, 'base.json')
SECRETS_LOCAL = os.path.join(SECRETS_DIR, 'local.json')
SECRETS_DEV = os.path.join(SECRETS_DIR, 'dev.json')
SECRETS_PRODUCTION = os.path.join(SECRETS_DIR, 'production.json')

secrets = json.loads(open(SECRETS_BASE, 'rt').read())


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')




AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!



def set_config(obj, module_name=None , start=False):

    def eval_obj(obj):
        # 객체가 int, float이거나
        if isinstance(obj, numbers.Number) or (
                # str형이면서 숫자 변환이 가능한 경우
                isinstance(obj, str) and obj.isdigit()):
            return obj
        # 객체가 int, float가 아니면서 숫자형태를 가진 str도 아닐경우
        try:
            return eval(obj)
        except NameError:
            # 없는 변수를 참조할 때 발생하는 예외
            return obj
        except Exception as e:
            # print(f'Cannot eval object({obj}), Exception:{e}')
            return obj

    # base.json파일을 parsing한 결과 (Python dict)를 순회
    # set_config에 전달된 객체가 'dict'형태일 경우
    if isinstance(obj, dict):
        # key, value를 순회
        for key, value in obj.items():
            # value가 dict이거나 list일 경우 재귀적으로 함수를 다시 실행
            # print(f'setconfig, key: {key}, value: {value}')
            if isinstance(value, dict) or isinstance(value, list):
                set_config(value)
            # 그 외의 경우 value를 평가한 값을 할당
            else:
                obj[key] = eval_obj(value)
            # set_config()가 처음 호출된 loop에서만 setattr()을 실행
            if start:
                setattr(sys.modules[module_name], key, value)
    # 전달된 객체가 'list'형태일 경우
    elif isinstance(obj, list):
        # list아이템을 순회하며
        for index, item in enumerate(obj):
            obj[index] = eval_obj(item)
    # print('== End ==')


setattr(sys.modules[__name__], 'raven', importlib.import_module('raven'))
set_config(secrets, module_name=__name__, start=True)




AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'members',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

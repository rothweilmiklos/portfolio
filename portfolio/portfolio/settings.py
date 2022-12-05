"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import os
from . import db_config

from .secret_key import get_secret_value

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
#       For development, uncomment the line below:
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

#       For production, uncomment the line below:
SECRET_KEY = get_secret_value('portfolio_secret_key')


# SECURITY WARNING: don't run with debug turned on in production!
#       For development uncomment the line below:
# DEBUG = 1 == int(os.environ.get('DEBUG'))

#     For development uncomment the two lines below:
DEBUG_VALUE = 1 == int(get_secret_value('debug'))
DEBUG = DEBUG_VALUE


ALLOWED_HOSTS = ['192.168.0.106', '127.0.0.1', 'portfolio']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig'
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

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'portfolio.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE = db_config.dev_or_prod_db(debug=DEBUG, base_directory=BASE_DIR)

DATABASES = {
    'default': DATABASE
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/portfolio/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django_ses.SESBackend'
# For development uncomment the two lines below, and comment out the 2 lines below that
# AWS_ACCESS_KEY_ID = 'AKIAUWY3QL2642QMND4L'
# AWS_SECRET_ACCESS_KEY = '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'
# For production uncomment the two lines below, and comment out the 2 lines above
AWS_ACCESS_KEY_ID = get_secret_value('aws_access_key')
AWS_SECRET_ACCESS_KEY = get_secret_value('aws_secret_key')

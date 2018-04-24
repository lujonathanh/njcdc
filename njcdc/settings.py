"""
Django settings for njcdc project.
Generated by 'django-admin startproject' using Django 2.0.3.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url
import django_heroku
from .settings_common import *

ALLOWED_HOSTS = [".herokuapp.com/", "127.0.0.1", "njcdc.herokuapp.com"]

# DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'njcdc',
        'USER': 'dcw3',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

<<<<<<< HEAD
=======
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())

SESSION_COOKIE_DOMAIN = "njcdc.herokuapp.com"

# deployment stuff
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_PRELOAD = True
DEBUG = False
>>>>>>> 90dd4e1a87cf39abbb26fb209717de0be64ece00

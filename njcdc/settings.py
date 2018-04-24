from njcdc.settings_common import *


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
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
>>>>>>> 2fe4cd33a253cf9908459a5f245fd9b100feda8a

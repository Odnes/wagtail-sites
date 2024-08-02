from .base import *

#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        #'PASSWORD': 'password1',
        'HOST': 'localhost', # shoud check postgresql.service
        'PORT': '5432',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m^a27y5pdf9lgo+e5$@e^n07rhv+v)jr(#y4n^06fb4^^s8wv-"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

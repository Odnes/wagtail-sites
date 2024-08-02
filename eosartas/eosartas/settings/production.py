from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "service": "my_service",
            "passfile": ".my_pgpass",
        },
    }
}

try:
    from .local import *
except ImportError:
    pass

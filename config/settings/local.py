from .base import *
from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES, env

# GENERAL
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "*"]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# TEMPLATES
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG
DISPLAY_OPENAPI_DOCS = True

# APPS AND MIDDLEWARE
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = ["127.0.0.1"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

INSTALLED_APPS += ["django_extensions"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"},
    },
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "asyncio": {"level": "WARNING"},
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "services.core": {"handlers": ["console"], "level": "INFO"},
        "django.db.backends": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}

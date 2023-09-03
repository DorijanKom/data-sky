import os
import re
from pathlib import Path
from kombu import Exchange, Queue

import environ
from django.utils.translation import gettext_lazy as _

ROOT_DIR = environ.Path(__file__) - 3  # (services/config/settings/base/base.py - 4 = services/)
APPS_DIR = ROOT_DIR.path("services")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path(".env")))

CACHE_OPTIONS_MAP = {
    "CLIENT_CLASS": "services.core.utils.custom_redis_client.CustomRedisClient",
    "IGNORE_EXCEPTIONS": True,
}

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = True

POSTGRES_DB = env("POSTGRES_DB")
POSTGRES_USER = env("POSTGRES_USER")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD")
POSTGRES_HOST = env("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT")

DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASES = {
    "default": env.db("DATABASE_URL", default=DATABASE_URL),
}

REDIS_URL = env("REDIS_URL", default=None)
if not REDIS_URL:
    REDIS_PASSWORD = env("REDIS_PASSWORD", default=None)
    REDIS_HOST = env("REDIS_HOST")
    REDIS_PORT = env.int("REDIS_PORT", 6379)

    if REDIS_PASSWORD:
        REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    else:
        REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default=REDIS_URL),
        "OPTIONS": CACHE_OPTIONS_MAP,
    }
}

WSGI_APPLICATION = "config.wsgi.application"

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django_celery_beat",
    "django_filters",
]
THIRD_PARTY_APPS = ["rest_framework", "corsheaders", "watchman", "drf_yasg", "rest_framework.authtoken"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "EXCEPTION_HANDLER": "services.core.utils.error_handler.custom_exception_handler",
    "PAGE_SIZE": 100,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

WATCHMAN_TOKEN_NAME = "health-service-token"
WATCHMAN_TOKENS = env("HEALTH_TOKENS")

WATCHMAN_CHECKS = (
    "watchman.checks.caches",
    "watchman.checks.databases",
)

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}

PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

RESOURCES_ROOT = str(ROOT_DIR("resources"))

STATIC_ROOT = str(ROOT_DIR("staticfiles"))

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    str(APPS_DIR.path("static")),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage"
    }
}

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")

MEDIA_ROOT = str(APPS_DIR("media"))

MEDIA_URL = "/media/"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

ADMIN_URL = env("ADMIN_URL", default="admin/")

INSTALLED_APPS += ["services.asyncq.celery.CeleryAppConfig"]
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=None)
if not CELERY_BROKER_URL:
    RABBITMQ_DEFAULT_USER = env("RABBITMQ_DEFAULT_USER")
    RABBITMQ_DEFAULT_PASS = env("RABBITMQ_DEFAULT_PASS")
    RABBITMQ_HOST = env("RABBITMQ_HOST")
    RABBITMQ_DEFAULT_VHOST = env("RABBITMQ_DEFAULT_VHOST")
    RABBITMQ_PORT = env("RABBITMQ_PORT")
    CELERY_BROKER_URL = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_DEFAULT_VHOST}"

CELERY_RESULT_BACKEND = None
CELERY_IGNORE_RESULT = True

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TASK_ACKS_LATE = True
CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

DISPLAY_OPENAPI_DOCS = env.bool("DISPLAY_OPENAPI_DOCS", False)

INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

# CORS SETTINGS
CORS_ALLOW_CREDENTIALS = env.bool("DJANGO_CORS_ALLOW_CREDENTIALS", default=True)
CORS_ORIGIN_WHITELIST = env.tuple("DJANGO_CORS_ORIGIN_WHITELIST")

CORW = env.str("DJANGO_CORS_ORIGIN_REGEX", default="")
CORS_ORIGIN_REGEX_WHITELIST = [CORW] if CORW else []

# CSRF_TRUSTED_ORIGINS = [re.sub(r"http[s]?://", "", route) for route in CORS_ORIGIN_WHITELIST]
CSRF_TRUSTED_ORIGINS = [route for route in CORS_ORIGIN_WHITELIST]
CSRF_COOKIE_DOMAIN = env("DJANGO_CSRF_COOKIE_DOMAIN", default=None)

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = env("SESSION_COOKIE_NAME")
SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN")

LANGUAGES = [
    ("en", _("English")),
]

LOCALE_PATHS = [
    os.path.join(APPS_DIR, "locale/"),
    os.path.join(APPS_DIR, "core/locale/"),
]

SITE_HOST = env("SITE_HOST")

default_exchange = Exchange("sinbad_default", type="direct")

CELERY_QUEUES = (
    Queue("sinbad_default", default_exchange, routing_key="sinbad_default", consumer_arguments={"x-priority": 0}),
)

CELERY_DEFAULT_QUEUE = "sinbad_default"

LOCAL_APPS = [
    "services.core.apps.CoreServiceConfig",
]

INSTALLED_APPS += LOCAL_APPS
AUTH_USER_MODEL = "core.User"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
CELERY_IMPORTS = ("services.asyncq.core_tasks",)

MIGRATION_MODULES = {
    "core": "services.core.migrations",
}

ROOT_URLCONF = "config.urls"

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '072fbebf596cbf'
EMAIL_HOST_PASSWORD = '20a273e38dbc8a'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOG_ERROR_TRACE = True
LOG_EXCEPTION = True

MAIL_SERVICE_CLASS = env(
    "MAIL_SERVICE_CLASS", default="services.core.utils.mailing_service.ExchangeMailService"
)

EXCHANGE_CLIENT_ID = env("EXCHANGE_CLIENT_ID", default=None)
EXCHANGE_CLIENT_SECRET = env("EXCHANGE_CLIENT_SECRET", default=None)
TOKEN_EXPIRATION_PERIOD = env.int("TOKEN_EXPIRATION_PERIOD", default=24)
OBTAIN_RATES_PERIOD = env.int("OBTAIN RATES PERIOD", default=30)
DATE_INPUT_FORMATS = ['%d-%m-%Y']

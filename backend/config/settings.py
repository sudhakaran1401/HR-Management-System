from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config( "DEBUG", cast=bool, default=False, )

ALLOWED_HOSTS = config( "ALLOWED_HOSTS", cast=lambda v: [host.strip() for host in v.split(",")], default="localhost", )

LANGUAGE_CODE = config( "LANGUAGE_CODE", default="en-us", )

TIME_ZONE = config( "TIME_ZONE", default="Asia/Kolkata", )

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
    "employees.apps.EmployeesConfig",
    "leave.apps.LeaveConfig",
    "attendance.apps.AttendanceConfig",
    "payroll.apps.PayrollConfig",
    "accounts.apps.AccountsConfig",
    "dashboard.apps.DashboardConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

STATIC_URL = config( "STATIC_URL", default="/static/", )

STATICFILES_DIRS = [ BASE_DIR / "static", ]

STATIC_ROOT = BASE_DIR / config( "STATIC_ROOT", default="staticfiles", )

# WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = config( "MEDIA_URL", default="/media/", )

MEDIA_ROOT = BASE_DIR / config( "MEDIA_ROOT", default="media", )

LOGIN_URL = config( "LOGIN_URL", default="login", )

LOGIN_REDIRECT_URL = config( "LOGIN_REDIRECT_URL", default="post_login_redirect", )

LOGOUT_REDIRECT_URL = config( "LOGOUT_REDIRECT_URL", default="/admin/login/", )

SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_NAME = config( "SESSION_COOKIE_NAME", default="hrms_session", )

SESSION_COOKIE_SECURE = config( "SESSION_COOKIE_SECURE", cast=bool, default=False, )

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = config( "CSRF_COOKIE_SECURE", cast=bool, default=False, )

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"

LOG_LEVEL = config( "LOG_LEVEL", default="INFO", )

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config( "ACCESS_TOKEN_LIFETIME", cast=int, default=60, )
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config( "REFRESH_TOKEN_LIFETIME", cast=int, default=2, )
    ),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "HR Management System API",
    "DESCRIPTION": "API documentation for the HR Management System.",
    "VERSION": "1.0.0",
}

CORS_ALLOWED_ORIGINS = config( "CORS_ALLOWED_ORIGINS", cast=lambda v: [origin.strip() for origin in v.split(",")], default="", )

CSRF_TRUSTED_ORIGINS = config( "CSRF_TRUSTED_ORIGINS", cast=lambda v: [origin.strip() for origin in v.split(",")], default="", )

CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = [ "Content-Disposition", ]

EMAIL_BACKEND = config( "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend", )

EMAIL_HOST = config("EMAIL_HOST")

EMAIL_PORT = config( "EMAIL_PORT", cast=int, default=587, )

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = config( "EMAIL_USE_TLS", cast=bool, default=True, )

EMAIL_USE_SSL = config( "EMAIL_USE_SSL", cast=bool, default=False, )

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

STORAGES = {
    "default": { "BACKEND": "django.core.files.storage.FileSystemStorage", },
    "staticfiles": { "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage", },
}

SECURE_BROWSER_XSS_FILTER = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG

X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = config( "SECURE_SSL_REDIRECT", cast=bool, default=False, )

SECURE_PROXY_SSL_HEADER = ( "HTTP_X_FORWARDED_PROTO", "https", )

USE_X_FORWARDED_HOST = True

SECURE_HSTS_SECONDS = config( "SECURE_HSTS_SECONDS", cast=int, default=0, )

SECURE_HSTS_INCLUDE_SUBDOMAINS = config( "SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=False, )

SECURE_HSTS_PRELOAD = config( "SECURE_HSTS_PRELOAD", cast=bool, default=False, )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}

# REDIS_URL = config("REDIS_URL", default=None)

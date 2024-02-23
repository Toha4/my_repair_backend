from datetime import timedelta
import os
from pathlib import Path

import environ


root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file
SITE_ROOT = root()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=True)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=str, default="localhost, 127.0.0.1").split(", ")


# Application definition

INSTALLED_APPS = [
    "authentication",
    "core",
    "homes",
    "shops",
    "purchases",
    "integrations.get_receipts",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'HOST': env("DB_HOST", cast=str),
        'NAME': env("DB_NAME", cast=str),
        'USER': env("DB_USER", cast=str),
        'PASSWORD': env("DB_PASS", cast=str),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 5,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "django_static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "authentication.CustomUser"


# Форматы даты/времени.
DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = " ".join((DATE_FORMAT, TIME_FORMAT))


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "app.pagination.BasePagination",
    "PAGE_SIZE": 50,
    "DATE_FORMAT:": DATE_FORMAT,
    "DATE_INPUT_FORMATS": [DATE_FORMAT, "iso-8601"],
    "TIME_FORMAT": TIME_FORMAT,
    "DATETIME_FORMAT": DATETIME_FORMAT,
}

AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=28),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SIMPLE_JWT_SIGNING_KEY", cast=str, default=SECRET_KEY),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": AUTH_HEADER_NAME,
    "USER_ID_FIELD": "pk",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "REFRESH_COOKIE_NAME": "refresh",
}


CORS_ORIGIN_ALLOW_ALL = env("CORS_ORIGIN_ALLOW_ALL", cast=bool, default=False)
CORS_ALLOW_CREDENTIALS = env("CORS_ALLOW_CREDENTIALS", cast=bool, default=True)
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST", cast=str, default="http://localhost:3000").split(", ")

# TODO: ВРЕМЕННО Api ключ сервиса по проверки чека https://proverkacheka.com 
PROVERKA_CHEKA_API_KEY = env("PROVERKA_CHEKA_API_KEY", cast=str, default='')

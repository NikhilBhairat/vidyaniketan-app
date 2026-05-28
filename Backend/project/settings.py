from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# SECURITY
# ----------------------------

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-in-production"
)

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    "vidyaniketan-app-main-f58e2f6.kuberns.cloud",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"

CSRF_TRUSTED_ORIGINS = [
    "https://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
    "http://vidyaniketan-app-main-f58e2f6.kuberns.cloud",
]

# IMPORTANT for Kubernetes / reverse proxy (CSRF fix)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False

# ----------------------------
# APPLICATIONS
# ----------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "django_filters",
    "corsheaders",

    "apps.accounts",
    "apps.students",
    "apps.attendance",
    "apps.fees",
    "apps.results",
    "apps.study_material",
    "apps.lectures",
    "apps.gallery",
    "apps.notifications",
    "apps.api",
]

# ----------------------------
# MIDDLEWARE (IMPORTANT ORDER)
# ----------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise for static files (FIX ADMIN CSS/JS)
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# CORS (OK for now, tighten later)
# ----------------------------

CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------
# URL / WSGI
# ----------------------------

ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

# ----------------------------
# TEMPLATES
# ----------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------------
# DATABASE
# ----------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ----------------------------
# AUTH
# ----------------------------

AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = []

# ----------------------------
# REST FRAMEWORK
# ----------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ----------------------------
# STATIC FILES (FIX ADMIN CSS/JS)
# ----------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise storage (IMPORTANT)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------
# MEDIA FILES
# ----------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------
# DEFAULT AUTO FIELD
# ----------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

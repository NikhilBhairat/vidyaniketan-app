from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# SECURITY
# ----------------------------

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-in-production"
)

# Debug will automatically be False on Render unless you set an environment variable DEBUG=True
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# Wildcard '*' allows Render internal health checks and external Flutter apps to connect seamlessly
ALLOWED_HOSTS = [
    "vidyaniketan-app-2.onrender.com",  # Your exact domain name
    "127.0.0.1",
    "localhost",
    "10.0.2.2",  # For Android emulator
    "*",
]

CSRF_COOKIE_SECURE = False  # Set to True later if enforcing strict HTTPS exclusively
SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Trusted origins specifically updated to reflect your active Render domain name without typos
CSRF_TRUSTED_ORIGINS = [
    "https://onrender.com",
    "http://onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://10.0.2.2:8000",  
]

# Important reverse proxy headers for proper SSL handshaking on Render
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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Handles static file delivery natively on Render
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# CORS
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

# Safe checking fallback prevents build failures if local global static asset folder does not exist
if os.path.exists(BASE_DIR / "static"):
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Gzip compresses and assets managed seamlessly by WhiteNoise
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

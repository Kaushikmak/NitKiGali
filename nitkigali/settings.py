import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'


ALLOWED_HOSTS = []
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL')
if RAILWAY_STATIC_URL:

    ALLOWED_HOSTS.append(RAILWAY_STATIC_URL.strip("https://").strip("/"))

VERCEL_DOMAIN = os.environ.get('VERCEL_DOMAIN')
if VERCEL_DOMAIN:
    ALLOWED_HOSTS.append(VERCEL_DOMAIN)

CSRF_TRUSTED_ORIGINS = []

# Add the Railway domain
if RAILWAY_STATIC_URL:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_STATIC_URL.strip('https://').strip('/')}")

# Add the Vercel domain
if VERCEL_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{VERCEL_DOMAIN}")


INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ws',
    
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nitkigali.urls'

ASGI_APPLICATION = 'nitkigali.asgi.application'


REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}



# --- DATABASE (FOR RAILWAY) ---
# This reads the DATABASE_URL provided by Railway's PostgreSQL plugin
DATABASES = {
    'default': dj_database_url.config(
        # Fallback to your sqlite3 db for local dev if DATABASE_URL isn't set
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
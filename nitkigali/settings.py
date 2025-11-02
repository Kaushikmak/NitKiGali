import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- PRODUCTION SECURITY ---
# Load the secret key from the .env file
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 
    'default-fallback-key-for-local-dev-only' # A fallback
)

# Load DEBUG from the .env file (defaults to False)
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Load allowed hosts from the .env file
# It expects a comma-separated string, e.g., "localhost,127.0.0.1,my-site.com"
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# --- END PRODUCTION SECURITY ---


# Application definition
INSTALLED_APPS = [
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nitkigali.wsgi.application'
ASGI_APPLICATION = 'nitkigali.asgi.application'

# --- REDIS CHANNEL LAYER ---
# (The 'InMemoryChannelLayer' definition has been removed)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # This must match the service name in docker-compose.yml
            "hosts": [("redis", 6379)],
        },
    },
}

# --- REDIS CACHE (Optional but recommended) ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        # Use a different DB (e.g., /1)
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ... (rest of your settings like AUTH_PASSWORD_VALIDATORS, etc.) ...

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Add STATIC_ROOT for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
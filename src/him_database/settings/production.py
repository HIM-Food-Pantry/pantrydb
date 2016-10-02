# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=him_client_database.settings.production

from .base import *  # NOQA

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]

# Must mention ALLOWED_HOSTS in production!
# ALLOWED_HOSTS = ["him_client_database.com"]

# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

SERVER_PORT = env('PORT')

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})



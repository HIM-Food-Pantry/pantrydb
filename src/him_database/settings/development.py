import dj_database_url

from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Django Debug Toolbar
INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
)

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = 'u8!7cbl_=e-2o=&513r^*nj)b+yqkd^tb2w^e1b3h93a)h14tv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

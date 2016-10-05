"""
WSGI config for him_database project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "him_database.settings.production")

import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.environ.get('INSTALL_PATH'))

application = get_wsgi_application()

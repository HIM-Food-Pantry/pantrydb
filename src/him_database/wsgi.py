"""
WSGI config for him_database project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from waitress import serve

sys.path.append(os.environ.get('INSTALL_PATH'))

application = get_wsgi_application()

if settings.DEBUG:
    application = get_wsgi_application()
else:
    """If not production/debug launch the waitress host"""
    serve(application, host='0.0.0.0', port=8000)

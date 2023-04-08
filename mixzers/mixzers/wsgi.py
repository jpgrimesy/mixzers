"""
WSGI config for mixzers project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mixzers.mixzers.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__))) + '/..'
sys.path.append('/app/mixzers')
sys.path.append('/app/mixzers/main_app')

application = get_wsgi_application()

"""
WSGI config for ItemManager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#PRODUCCION:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ItemManager.settingsProd')
os.environ.setdefault('DESARROLLO', 'false')

#DESARROLLO
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ItemManager.settings')
#os.environ.setdefault('DESARROLLO', 'true')


application = get_wsgi_application()

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting.settings')
sys.path.append('/opt/accounting')
application = get_wsgi_application()

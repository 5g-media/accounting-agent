import os

# =================================
# ENG ACCOUNTING SETTINGS
# =================================
ACCOUNTING = {
    'PROTOCOL': os.getenv('ACC_BILLING_PROTOCOL'),
    'HOST': os.getenv('ACC_BILLING_IP'),
    'PORT': os.getenv('ACC_BILLING_PORT')
}

BASE_URL = '{}://{}:{}/api/accounting'.format(ACCOUNTING['PROTOCOL'], ACCOUNTING['HOST'], ACCOUNTING['PORT'])
AUTH_URL = '{}://{}:{}/api/authenticate'.format(ACCOUNTING['PROTOCOL'], ACCOUNTING['HOST'], ACCOUNTING['PORT'])

ACCOUNTING_USERNAME = os.getenv('ACC_BILLING_USERNAME')
ACCOUNTING_PASSWORD = os.getenv('ACC_BILLING_PASSWORD')

CLOSE_SESSIONS = {
    'ns': '/closeNsSession',
    'vnf': '/closeVnfSession',
    'vdu': '/closeVduSession'
}

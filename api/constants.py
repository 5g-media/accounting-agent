from django.conf import settings

# =================================
#    DB INSTANCE DEFAULT VALUES
# =================================
CATALOG_USER_DEFAULT = 'catdev1'
CATALOG_TENANT_DEFAULT = 'default'
MANO_ID_DEFAULT = settings.MANO_ID
MANO_PROJECT_DEFAULT = 'default'
NFVIPOP_ID_DEFAULT = settings.NFVIPOP_ID

# =================================
#      DB VDU DEFAULT VALUES
# =================================
FLAVOR_DEFAULT = 'X_X_XX'

# =================================
#           VIM TYPES
# =================================
OPENSTACK = 'openstack'
OPENNEBULA = 'opennebula'
KUBERNETES = 'faas'

# =================================
#       OSM OPERATION TYPES
# =================================
INSTANTIATE = 'instantiate'
INSTANTIATED = 'instantiated'
TERMINATE = 'terminate'
TERMINATED = 'terminated'
SCALE = 'scale'
SCALED = 'scaled'
SCALE_IN = 'SCALE_IN'
SCALE_OUT = 'SCALE_OUT'

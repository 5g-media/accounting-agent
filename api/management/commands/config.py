from django.conf import settings

# =================================
# KAFKA SETTINGS
# =================================
KAFKA_SERVER = settings.OSM_KAFKA_BOOTSTRAP
KAFKA_CLIENT_ID = 'osm-notification-handler'
KAFKA_GROUP_ID = 'MON_ACC'
KAFKA_API_VERSION = (0, 10, 1)
KAFKA_TOPICS = ['ns', ]

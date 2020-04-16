from django.conf import settings

# =================================
# WHITE LIST OF MONITORING METRICS
# =================================
METRICS_WHITE_LIST = [
    'memory.usage',
    'disk.usage',
    'cpu_util',
    'container_memory_usage_bytes',
    'memory',
    'disksize'
]

# =================================
# KAFKA SETTINGS
# =================================
KAFKA_SERVER = settings.BOOTSTRAP_SERVER
KAFKA_CLIENT_ID = 'accounting-metric-collector'
KAFKA_GROUP_ID = 'MON_ACC'
KAFKA_API_VERSION = (0, 10, 1)
KAFKA_TRANSLATION_TOPIC = 'ns.instances.trans'

# =================================
# METRICS DICTIONARIES
# =================================
METRICS_DICT = {
    'memory.usage': 'MEMORY_MB',
    'cpu_util': 'CPU_CYCLE',
    'disk.usage': 'DISK_GB',
    'container_memory_usage_bytes': 'MEMORY_MB',
    'memory': 'MEMORY_MB',
    'disksize': 'DISK_GB'
}

import json
import logging

from django.core.management import BaseCommand
from kafka import KafkaConsumer

from api.models import Vdu, VduMetric
from .config import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, METRICS_WHITE_LIST, METRICS_DICT, KAFKA_GROUP_ID, \
    KAFKA_TRANSLATION_TOPIC

logger = logging.getLogger(__name__)


def metric_collector():
    """Connects on Kafka Bus and collects metrics sent for active VDUs."""
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, enable_auto_commit=True,
                             value_deserializer=lambda v: json.loads(v.decode('utf-8', 'ignore')),
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_GROUP_ID)
    consumer.subscribe(topics=[KAFKA_TRANSLATION_TOPIC])
    logger.info('Initialized Kafka Consumer & subscribed to topics')

    for msg in consumer:

        # Get metric and check if it is in whitelist
        metric = msg.value['metric']
        if metric['name'] not in METRICS_WHITE_LIST:
            continue

        # Get VDU id and check if it exists
        vdu_uuid = msg.value['mano']['vdu']['id']
        vdu = Vdu.objects.select_related('tenant', 'instance', 'vnf').filter(uuid=vdu_uuid, state='active')
        if not vdu.exists():
            continue
        logger.debug('Metric: {}, Vdu: {}'.format(metric, vdu_uuid))

        # If it exists create metric for this vdu
        VduMetric.objects.create(vdu=vdu[0], metric_name=METRICS_DICT[metric['name']], metric_value=metric['value'])
        logger.info('Received and saved {} metric for vdu {}'.format(METRICS_DICT[metric['name']], vdu_uuid))


class Command(BaseCommand):
    def handle(self, *args, **options):
        metric_collector()

import logging

import yaml
from django.core.management import BaseCommand
from kafka import KafkaConsumer

from api.constants import INSTANTIATE, TERMINATE, INSTANTIATED, TERMINATED, SCALE, SCALED, SCALE_OUT, SCALE_IN
from api.models import Instance
from api.utils import ns_termination_handler, ns_instantiation_handler, ns_pre_instantiation_handler, \
    vnf_scaling_out_handler, vnf_scaling_in_handler
from .config import KAFKA_SERVER, KAFKA_CLIENT_ID, KAFKA_API_VERSION, KAFKA_GROUP_ID, KAFKA_TOPICS

logger = logging.getLogger(__name__)


def osm_notification_handler():
    """Connects on OSM Kafka Bus and subscribes to NS-related topics."""
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, client_id=KAFKA_CLIENT_ID, enable_auto_commit=True,
                             value_deserializer=lambda v: yaml.safe_load(v.decode('utf-8', 'ignore')),
                             api_version=KAFKA_API_VERSION, group_id=KAFKA_GROUP_ID)
    consumer.subscribe(KAFKA_TOPICS)
    logger.info('Initialized Kafka Consumer & subscribed to OSM topics')

    for msg in consumer:

        # Get operation type from key
        operation = msg.key.decode('ascii')
        message = msg.value
        if operation == INSTANTIATE:
            logger.info('Instantiation of NS with UUID {} started'.format(message['nsInstanceId']))
            ns_pre_instantiation_handler(message['operationParams'])
        elif operation == TERMINATE:
            logger.info('Termination of NS with UUID {} started'.format(message['nsInstanceId']))
            ns = Instance.objects.filter(uuid=message['nsInstanceId'])
            if ns.exists():
                ns.update(state='terminate')
        elif operation == SCALE:
            scale_vnf_type = message['operationParams']['scaleVnfData']['scaleVnfType']
            if scale_vnf_type == SCALE_OUT:
                logger.info('Scaling-out VNF of NS with UUID {} started'.format(message['nsInstanceId']))
            elif scale_vnf_type == SCALE_IN:
                logger.info('Scaling-in VNF of NS with UUID {} started'.format(message['nsInstanceId']))
        elif operation == INSTANTIATED:
            ns = Instance.objects.filter(uuid=message['nsr_id'])
            if ns.exists():
                if message['operationState'] == 'COMPLETED':
                    ns.update(state='active')
                    ns_instantiation_handler(ns[0])
                    logger.info('Instantiation of NS with UUID {} completed'.format(ns[0].uuid))
                elif message['operationState'] == 'FAILED':
                    logger.info('Instantiation of NS with UUID {} failed'.format(ns[0].uuid))
                    ns.delete()
        elif operation == TERMINATED:
            ns = Instance.objects.filter(uuid=message['nsr_id'])
            if ns.exists():
                if message['operationState'] == 'COMPLETED':
                    ns.update(state='deleted')
                    ns_termination_handler(ns[0])
                    logger.info('Termination of NS with UUID {} completed'.format(ns[0].uuid))
                elif message['operationState'] == 'FAILED':
                    ns.update(state='active')
                    logger.info('Termination of NS with UUID {} failed'.format(ns[0].uuid))
        elif operation == SCALED:
            ns = Instance.objects.filter(uuid=message['nsr_id'])
            if ns.exists():
                if scale_vnf_type == SCALE_OUT:
                    if message['operationState'] == 'COMPLETED':
                        vnf_scaling_out_handler(ns[0])
                        logger.info('Scaling-out VNF of NS with UUID {} completed'.format(ns[0].uuid))
                    elif message['operationState'] == 'FAILED':
                        logger.info('Scaling-out VNF of NS with UUID {} failed'.format(ns[0].uuid))
                elif scale_vnf_type == SCALE_IN:
                    if message['operationState'] == 'COMPLETED':
                        vnf_scaling_in_handler(ns[0])
                        logger.info('Scaling-in VNF of NS with UUID {} completed'.format(ns[0].uuid))
                    elif message['operationState'] == 'FAILED':
                        logger.info('Scaling-in VNF of NS with UUID {} failed'.format(ns[0].uuid))


class Command(BaseCommand):
    def handle(self, *args, **options):
        osm_notification_handler()

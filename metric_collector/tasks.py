import logging

from django.db.models import Avg

from accounting.celery import app
from accounting_client.accounting_client import accounting_client
from api.models import Vdu, VduMetric

logger = logging.getLogger(__name__)


@app.task
def send_metrics():
    """Aggregate and send metrics per VDU to consumption logger."""

    # Logging execution
    logger.info('Preparing to aggregate and send metrics for active vdus')

    # Fetch all active VDUs
    vdus = Vdu.objects.select_related('tenant', 'instance', 'vnf').filter(state='active')

    for vdu in vdus:

        # Metrics for vdu
        vdu_metrics = VduMetric.objects.select_related('vdu').filter(vdu__uuid=vdu.uuid)

        # Average of cpu cycles measurements
        cpu_cycle = vdu_metrics.filter(metric_name='CPU_CYCLE')
        if cpu_cycle.exists():
            cpu_cycle_avg = cpu_cycle.aggregate(Avg('metric_value'))['metric_value__avg']
            logger.info('Vdu: {}, Average Cpu Util: {}'.format(vdu.uuid, cpu_cycle_avg))
            accounting_client.log_vdu_consumption('CPU_CYCLE', cpu_cycle_avg, vdu.vdu_session_id)

        # Average of ram megabytes measurements
        ram_mb = vdu_metrics.filter(metric_name='MEMORY_MB')
        if ram_mb.exists():
            ram_mb_avg = ram_mb.aggregate(Avg('metric_value'))['metric_value__avg']
            logger.info('Vdu: {}, Average Memory in MB: {}'.format(vdu.uuid, ram_mb_avg))
            accounting_client.log_vdu_consumption('MEMORY_MB', ram_mb_avg, vdu.vdu_session_id)

        # Average of disk GB measurements
        disk_gb = vdu_metrics.filter(metric_name='DISK_GB')
        if disk_gb.exists():
            disk_gb_avg = disk_gb.aggregate(Avg('metric_value'))['metric_value__avg']
            logger.info('Vdu: {}, Average Disk in GB: {}'.format(vdu.uuid, disk_gb_avg / (1024 ** 3)))
            accounting_client.log_vdu_consumption('DISK_GB', disk_gb_avg / (1024 ** 3), vdu.vdu_session_id)

    # Delete all previous metrics
    VduMetric.objects.select_related('vdu').all().delete()

    logger.info('Finished aggregation and deleted previously collected metrics')
    return

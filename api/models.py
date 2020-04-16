from django.db import models

from accounting.settings import MAX_STR_LEN, MID_STR_LEN, MIN_STR_LEN
from api.constants import CATALOG_USER_DEFAULT, CATALOG_TENANT_DEFAULT, MANO_ID_DEFAULT, MANO_PROJECT_DEFAULT, \
    NFVIPOP_ID_DEFAULT, FLAVOR_DEFAULT


class Tenant(models.Model):
    """ Tenant Model. """
    created_at = models.DateTimeField(auto_now_add=True, help_text='Datetime of Tenant\'s creation')
    description = models.CharField(max_length=MAX_STR_LEN, null=True, help_text='Description of Tenant')
    name = models.CharField(max_length=MID_STR_LEN, null=True, help_text='Tenant\'s Name')
    uuid = models.CharField(max_length=MID_STR_LEN, null=True, help_text='Tenant\'s OSM UUID')


class Instance(models.Model):
    """ NS Instance Model. """
    tenant = models.ForeignKey(
        Tenant,
        related_name="instances",
        on_delete=models.CASCADE,
        null=True,
        help_text="NS Instance\'s Tenant",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text='Datetime of NS Instance\'s Creation')
    catalog_user = models.CharField(max_length=MID_STR_LEN, default=CATALOG_USER_DEFAULT, help_text='Catalog User')
    catalog_tenant = models.CharField(max_length=MID_STR_LEN, default=CATALOG_TENANT_DEFAULT, help_text='Catalog Tenant')
    description = models.CharField(max_length=MAX_STR_LEN, null=True, help_text='Description of NS Instance')
    mano_id = models.CharField(max_length=MID_STR_LEN, default=MANO_ID_DEFAULT, help_text='The MANO URL')
    mano_project = models.CharField(max_length=MID_STR_LEN, default=MANO_PROJECT_DEFAULT, help_text='The MANO Project')
    mano_user = models.CharField(max_length=MID_STR_LEN, null=True, help_text='The user of the MANO')
    name = models.CharField(max_length=MID_STR_LEN, null=True, help_text='NS Instance\'s Name')
    nfvipop_id = models.CharField(max_length=MID_STR_LEN, default=NFVIPOP_ID_DEFAULT)
    ns_session_id = models.IntegerField(default=-1, help_text='NS Instance\'s Session ID')
    state = models.CharField(max_length=MIN_STR_LEN, null=True, help_text='NS Instance\'s State')
    uuid = models.CharField(max_length=MID_STR_LEN, null=True, help_text='NS Instance\'s OSM UUID')
    vim_type = models.CharField(max_length=MIN_STR_LEN, null=True, help_text='NS Instance\'s VIM Type')


class Vnf(models.Model):
    """ VNF Model. """
    tenant = models.ForeignKey(
        Tenant,
        related_name='vnfs',
        on_delete=models.CASCADE,
        help_text='VNF\'s Tenant'
    )
    instance = models.ForeignKey(
        Instance,
        related_name='vnfs',
        on_delete=models.CASCADE,
        help_text='VNF\'s NS Instance'
    )
    creation_date = models.DateTimeField(auto_now_add=True, help_text='Datetime of VNF\'s Creation')
    name = models.CharField(max_length=MID_STR_LEN, help_text='VNF\'s Name', null=True)
    state = models.CharField(max_length=MIN_STR_LEN, help_text='VNF\'s State', null=True)
    uuid = models.CharField(max_length=MID_STR_LEN, help_text='VNF\'s OSM UUID', null=True)
    vim_type = models.CharField(max_length=MIN_STR_LEN, null=True, help_text='VNF\'s VIM Type')
    vnf_session_id = models.IntegerField(default=-1, help_text='VNF\'s Session ID')


class Vdu(models.Model):
    """ VDU Model. """
    tenant = models.ForeignKey(
        Tenant,
        related_name='vdus',
        on_delete=models.CASCADE,
        help_text='VDU\'s Tenant'
    )
    instance = models.ForeignKey(
        Instance,
        related_name='vdus',
        on_delete=models.CASCADE,
        help_text='VDU\'s NS Instance'
    )
    vnf = models.ForeignKey(
        Vnf,
        related_name='vdus',
        on_delete=models.CASCADE,
        help_text='VDU\'s VNF'
    )
    creation_date = models.DateTimeField(auto_now_add=True, help_text='Datetime of VDU\'s Creation')
    flavor = models.CharField(max_length=MIN_STR_LEN, default=FLAVOR_DEFAULT, help_text='VDU\'s Flavor')
    nfvipop_id = models.CharField(max_length=MID_STR_LEN, null=True, default=NFVIPOP_ID_DEFAULT)
    project_name = models.CharField(max_length=MID_STR_LEN, null=True, help_text='VDU\'s Project Name')
    state = models.CharField(max_length=MIN_STR_LEN, null=True, help_text='VDU\'s State')
    uuid = models.CharField(max_length=MID_STR_LEN, null=True, help_text='VDU\'s VIM UUID')
    vcpu = models.IntegerField(null=True, help_text='VDU\'s CPU')
    vdisk = models.IntegerField(null=True, help_text='VDU\'s Disk')
    vram = models.FloatField(null=True, help_text='VDU\'s RAM (GB)')
    vdu_session_id = models.IntegerField(default=-1, null=True, help_text='VDU\'s Session ID')
    vim_type = models.CharField(max_length=MIN_STR_LEN, null=True, help_text='VDU\'s VIM Type')


class VduMetric(models.Model):
    """ VDU Metric Model. """
    vdu = models.ForeignKey(
        Vdu,
        related_name='metrics',
        on_delete=models.CASCADE,
        help_text='Metrics of VDU'
    )
    metric_name = models.CharField(max_length=MID_STR_LEN, null=True, help_text='The Metric\'s Type')
    metric_value = models.FloatField(default=0.0, help_text='The Metric\'s Value')

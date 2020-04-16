import logging

from django.conf import settings
from rest_framework.status import HTTP_200_OK

from accounting_client.accounting_client import accounting_client
from api.constants import NFVIPOP_ID_DEFAULT
from api.models import Tenant, Vdu, Instance, Vnf
from nbiapi.identity import bearer_token
from nbiapi.nslcm import NsLcm
from nbiapi.osm_admin import OsmAdmin
from nbiapi.vnfpkgm import VnfPkgM
from openmanoapi.instances import Instance as OsmInstance
from openmanoapi.tenants import Tenant as OsmTenant

logger = logging.getLogger(__name__)


def ns_pre_instantiation_handler(ns_params):
    """Handles instantiation of NS before deployment of VDUs is completed.

    Args:
        ns_params (dict): Operation Parameters collected from Kafka

    """
    Instance.objects.create(description=ns_params.get('nsDescription', 'Default Description'), name=ns_params['nsName'],
                            uuid=ns_params['nsInstanceId'], nfvipop_id=ns_params['vimAccountId'], state='instantiate')


def ns_instantiation_handler(ns):
    """Handles instantiation of NS when deployment of VDUs completes.

    Args:
        ns (obj): The NS object under instantiation

    """
    # Get auth token from NBI
    token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'),
                         settings.OSM_ADMIN_CREDENTIALS.get('password'))

    # Get RO id for current NS
    nslcm, osm_admin, vnfpkgm = NsLcm(token), OsmAdmin(token), VnfPkgM(token)
    ns_response = nslcm.get_ns(ns.uuid)
    if ns_response.status_code != HTTP_200_OK:
        logger.info('NS with UUID {} no longer exists. Aborting instantiation'.format(ns.uuid))
        ns_object = Instance.objects.filter(uuid=ns.uuid)
        ns_object.update(state='deleted')
        return
    ns_info = ns_response.json()
    nsr_id = ns_info['_admin']['deployed']['RO']['nsr_id']

    # Find tenant to whom this NS belongs
    tenants = OsmTenant().get_list().json()['tenants']
    for tenant in tenants:

        # Check if tenant exists as an object
        tn = Tenant.objects.filter(uuid=tenant['uuid'])
        if not tn.exists():
            Tenant.objects.create(created_at=tenant['created_at'], description=tenant['description'],
                                  uuid=tenant['uuid'], name=tenant['name'])
            logger.info('Created new tenant object with uuid {}'.format(tenant['uuid']))
        tn = Tenant.objects.get(uuid=tenant['uuid'])

        # Check if NS belongs to current tenant
        ns_current = OsmInstance().get(tenant['uuid'], nsr_id)
        if ns_current.status_code != HTTP_200_OK:
            continue

        # Get VIM Information
        vim_data = osm_admin.get_vim(ns.nfvipop_id).json()

        # Update NS Information
        ns.tenant = tn
        ns.mano_user = tn.name
        ns.mano_project = ns_info['_admin']['projects_read'][0]
        # TODO: Change accordingly in case of central OSM
        ns.nfvipop_id = NFVIPOP_ID_DEFAULT
        ns.vim_type = vim_data['vim_type']
        ns.ns_session_id = accounting_client.open_ns_session(ns)
        ns.save()

        logger.info('New NS instance object: {}, Tenant: {}'.format(ns.uuid, tn.uuid))

        # Get VNFs of NS
        vnfs = nslcm.get_vnf_list_by_ns(ns.uuid).json()

        for vnf in vnfs:

            # VNF Name
            vnf_name = '{}.{}'.format(vnf['vnfd-ref'], vnf['member-vnf-index-ref'])

            # Get VM Flavor
            # TODO: Fix if VNFs include more than one VDU
            vm_flavor = vnfpkgm.get_vnfd(vnf['vnfd-id']).json()['vdu'][0]['vm-flavor']

            # Create and open VNF session
            v = Vnf.objects.create(
                tenant=tn, instance=ns, uuid=vnf['id'], name=vnf_name, state='active', vim_type=ns.vim_type)
            v.vnf_session_id = accounting_client.open_vnf_session(ns.ns_session_id, v.uuid, v.name)
            v.save()

            logger.info('New VNF object: {}, NS instance: {}'.format(v.uuid, ns.uuid))

            for vdur in vnf['vdur']:
                vdu = Vdu.objects.create(
                    tenant=tn, instance=ns, vnf=v, uuid=vdur['vim-id'], nfvipop_id=ns.nfvipop_id, state='active',
                    project_name=ns.mano_project, vcpu=vm_flavor['vcpu-count'], vram=vm_flavor['memory-mb'],
                    vdisk=vm_flavor['storage-gb'], vim_type=ns.vim_type,
                    flavor='{}_{}_{}'.format(vm_flavor['vcpu-count'], vm_flavor['memory-mb'], vm_flavor['storage-gb']))
                vdu.vdu_session_id = accounting_client.open_vdu_session(v.vnf_session_id, vdu)
                vdu.save()

                logger.info('New VDU object: {}, VNF: {}, NS: {}'.format(vdu.uuid, v.uuid, ns.uuid))
        break


def ns_termination_handler(ns):
    """Handles termination of NS and closes related sessions on the Billing Services.

    Args:
        ns (obj): The NS under termination

    """
    vnfs = Vnf.objects.select_related('tenant', 'instance').prefetch_related('vdus').filter(instance__uuid=ns.uuid)
    vdus = Vdu.objects.select_related('tenant', 'instance', 'vnf').filter(instance__uuid=ns.uuid)
    vnfs.update(state='deleted')
    vdus.update(state='deleted')
    for vdu in vdus:
        accounting_client.close_session(vdu.vdu_session_id, 'vdu')
    for vnf in vnfs:
        accounting_client.close_session(vnf.vnf_session_id, 'vnf')
    accounting_client.close_session(ns.ns_session_id, 'ns')
    logger.info('NS with uuid {} was deleted'.format(ns.uuid))


def vnf_scaling_out_handler(ns):
    """Handlers the scaling-out of a VNF and opens related sessions on the Billing Services.

    Args:
         ns (Instance): The NS under VNF-Scaling

    """
    # Get auth token from NBI
    token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'),
                         settings.OSM_ADMIN_CREDENTIALS.get('password'))

    # Get VNFs of NS & Tenant
    nslcm, vnfpkgm = NsLcm(token), VnfPkgM(token)
    vnfs = nslcm.get_vnf_list_by_ns(ns.uuid).json()
    tn = Tenant.objects.get(uuid=ns.tenant.uuid)

    for vnf in vnfs:

        # Get VNF
        v = Vnf.objects.get(uuid=vnf['id'])

        # Get VM Flavor
        # TODO: Fix if VNFs include more than one VDU
        vm_flavor = vnfpkgm.get_vnfd(vnf['vnfd-id']).json()['vdu'][0]['vm-flavor']

        # Check if VDU of scaled VNF is found
        vdu_is_created = False

        for vdur in vnf['vdur']:
            vdu_object = Vdu.objects.filter(uuid=vdur['vim-id'])
            if vdu_object.exists():
                continue
            vdu = Vdu.objects.create(
                tenant=tn, instance=ns, vnf=v, uuid=vdur['vim-id'], nfvipop_id=ns.nfvipop_id, state='active',
                project_name=ns.mano_project, vcpu=vm_flavor['vcpu-count'], vram=vm_flavor['memory-mb'],
                vdisk=vm_flavor['storage-gb'], vim_type=ns.vim_type,
                flavor='{}_{}_{}'.format(vm_flavor['vcpu-count'], vm_flavor['memory-mb'], vm_flavor['storage-gb']))
            vdu.vdu_session_id = accounting_client.open_vdu_session(v.vnf_session_id, vdu)
            vdu.save()
            vdu_is_created = True

            logger.info('New VDU object: {}, VNF: {}, NS: {}'.format(vdu.uuid, v.uuid, ns.uuid))

        if vdu_is_created:
            break


def vnf_scaling_in_handler(ns):
    """Handles scaling-in of NS and closes related sessions on the Billing Services.

    Args:
         ns (Instance): The NS under VNF-Scaling In

    """

    # Get auth token from NBI
    token = bearer_token(settings.OSM_ADMIN_CREDENTIALS.get('username'),
                         settings.OSM_ADMIN_CREDENTIALS.get('password'))

    # Get VNF UUIDs of NS & Tenant
    nslcm = NsLcm(token)
    vnfs = nslcm.get_vnf_list_by_ns(ns.uuid).json()

    for vnf in vnfs:
        vnf_object = Vnf.objects.get(uuid=vnf['id'])
        vdu_object_ids = [vdu.uuid for vdu in vnf_object.vdus.all()]
        vdu_vdur_ids = [vdur['vim-id'] for vdur in vnf['vdur']]
        vdu_scaled_in_ids = [x for x in vdu_object_ids if x not in vdu_vdur_ids]
        if len(vdu_scaled_in_ids) == 0:
            continue
        else:
            vdu_scaled_in_id = vdu_scaled_in_ids[0]
            vdus = Vdu.objects.select_related('tenant', 'instance', 'vnf').filter(uuid=vdu_scaled_in_id)
            vdus.update(state='deleted')
            accounting_client.close_session(vdus[0].vdu_session_id, 'vdu')
            logger.info('VDU with UUID {} was deleted'.format(vdus[0].uuid))
            break

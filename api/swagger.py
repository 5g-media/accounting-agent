from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from api.serializers import *

# ==================================
#     Accounting API Responses
# ==================================
TenantList_GET = {
    status.HTTP_200_OK: TenantSerializer(many=True),
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access tenants',
    status.HTTP_404_NOT_FOUND: 'Information not found',
}

TenantDetail_GET = {
    status.HTTP_200_OK: TenantSerializer,
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access tenant',
    status.HTTP_404_NOT_FOUND: 'Requested tenant not found',
}

InstanceList_GET = {
    status.HTTP_200_OK: InstanceSerializer(many=True),
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access instances',
    status.HTTP_404_NOT_FOUND: 'Information not found',
}

InstanceDetail_GET = {
    status.HTTP_200_OK: InstanceSerializer,
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access instance',
    status.HTTP_404_NOT_FOUND: 'Requested instance not found',
}

VnfList_GET = {
    status.HTTP_200_OK: VnfSerializer(many=True),
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access VNFs',
    status.HTTP_404_NOT_FOUND: 'Information not found',
}

VnfDetail_GET = {
    status.HTTP_200_OK: VnfSerializer,
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access VNF',
    status.HTTP_404_NOT_FOUND: 'Requested VNF not found',
}

VduList_GET = {
    status.HTTP_200_OK: VduSerializer(many=True),
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access VDUs',
    status.HTTP_404_NOT_FOUND: 'Information not found',
}

VduDetail_GET = {
    status.HTTP_200_OK: VduSerializer,
    status.HTTP_401_UNAUTHORIZED: 'Unauthorized to access VDU',
    status.HTTP_404_NOT_FOUND: 'Requested VDU not found',
}

# ==================================
#    Accounting API Parameters
# ==================================
TENANT_UUID = openapi.Parameter(
    name='tenant_uuid', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='The UUID of the Tenant',
    required=True
)

INSTANCE_UUID = openapi.Parameter(
    name='instance_uuid', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='The UUID of the NS Instance',
    required=True
)

VNF_UUID = openapi.Parameter(
    name='vnf_uuid', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='The UUID of the VNF',
    required=True
)

VDU_UUID = openapi.Parameter(
    name='vdu_uuid', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='The UUID of the VDU',
    required=True
)

UUID = openapi.Parameter(
    name='uuid', in_=openapi.IN_PATH,
    type=openapi.TYPE_STRING,
    description='The UUID of the entity to retrieve',
    required=True
)

# ==================================
#    Instance Swagger Decorators
# ==================================
instance_list = swagger_auto_schema(operation_description='List Instances', responses=InstanceList_GET)
instance_retrieve = \
    swagger_auto_schema(operation_description='Retrieve Instance', responses=InstanceDetail_GET)
instance_retrieve_by_uuid = \
    swagger_auto_schema(operation_description='Retrieve NS Instance by UUID', responses=InstanceDetail_GET)
instance_list_by_tenant_uuid = \
    swagger_auto_schema(operation_description='List NS Instances by Tenant UUID',
                        responses=InstanceList_GET, manual_parameters=[TENANT_UUID])
instance_retrieve_by_tenant_uuid = \
    swagger_auto_schema(operation_description='Retrieve NS Instance by Tenant UUID',
                        responses=InstanceDetail_GET, manual_parameters=[TENANT_UUID, UUID])

# ==================================
#     Tenant Swagger Decorators
# ==================================
tenant_list = swagger_auto_schema(operation_description='List Tenants', responses=TenantList_GET)
tenant_retrieve = swagger_auto_schema(operation_description='Retrieve Tenant', responses=TenantDetail_GET)
tenant_retrieve_by_uuid = swagger_auto_schema(
    operation_description='Retrieve Tenant by UUID', responses=TenantDetail_GET)

# ==================================
#      VNF Swagger Decorators
# ==================================
vnf_list = swagger_auto_schema(operation_description='List VNFs', responses=VnfList_GET)
vnf_retrieve = swagger_auto_schema(operation_description='Retrieve VNF', responses=VnfDetail_GET)
vnf_retrieve_by_uuid = swagger_auto_schema(operation_description='Retrieve VNF by UUID', responses=VnfDetail_GET)
vnf_list_by_tenant_uuid = swagger_auto_schema(
    operation_description='List VNFs by Tenant UUID', responses=VnfList_GET, manual_parameters=[TENANT_UUID])
vnf_retrieve_by_tenant_uuid = swagger_auto_schema(
    operation_description='Retrieve VNF by Tenant UUID', responses=VnfDetail_GET, manual_parameters=[TENANT_UUID, UUID])
vnf_list_by_instance_uuid = swagger_auto_schema(
    operation_description='List VNFs by NS Instance UUID', responses=VnfList_GET, manual_parameters=[INSTANCE_UUID])
vnf_retrieve_by_instance_uuid = \
    swagger_auto_schema(operation_description='Retrieve VNF by NS Instance UUID',
                        responses=VnfDetail_GET, manual_parameters=[INSTANCE_UUID, UUID])

# ==================================
#      VDU Swagger Decorators
# ==================================
vdu_list = swagger_auto_schema(operation_description='List VDUs', responses=VduList_GET)
vdu_retrieve = swagger_auto_schema(operation_description='Retrieve VDU', responses=VduDetail_GET)
vdu_retrieve_by_uuid = swagger_auto_schema(operation_description='Retrieve VDU by UUID', responses=VduDetail_GET)
vdu_list_by_tenant_uuid = swagger_auto_schema(
    operation_description='List VDUs by Tenant UUID', responses=VduList_GET, manual_parameters=[TENANT_UUID])
vdu_retrieve_by_tenant_uuid = swagger_auto_schema(
    operation_description='Retrieve VDU by Tenant UUID', responses=VduDetail_GET, manual_parameters=[TENANT_UUID, UUID])
vdu_list_by_instance_uuid = swagger_auto_schema(
    operation_description='List VDUs by NS Instance UUID', responses=VduList_GET, manual_parameters=[INSTANCE_UUID])
vdu_retrieve_by_instance_uuid = \
    swagger_auto_schema(operation_description='Retrieve VDU by NS Instance UUID',
                        responses=VduDetail_GET, manual_parameters=[INSTANCE_UUID, UUID])

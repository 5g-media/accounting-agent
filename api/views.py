import logging

from django.utils.decorators import method_decorator
from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from api.serializers import *
import api.swagger as swagger_decorators

logger = logging.getLogger(__name__)


@method_decorator(name='list', decorator=swagger_decorators.instance_list)
@method_decorator(name='retrieve', decorator=swagger_decorators.instance_retrieve)
class InstanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ Instance (Network Service) Resource """
    queryset = Instance.objects.select_related('tenant').prefetch_related('vnfs', 'vdus').all()
    serializer_class = InstanceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


@method_decorator(name='list', decorator=swagger_decorators.tenant_list)
@method_decorator(name='retrieve', decorator=swagger_decorators.tenant_retrieve)
class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    """ Tenant Resource """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


@method_decorator(name='list', decorator=swagger_decorators.vnf_list)
@method_decorator(name='retrieve', decorator=swagger_decorators.vnf_retrieve)
class VnfViewSet(viewsets.ReadOnlyModelViewSet):
    """ VNF Resource """
    queryset = Vnf.objects.select_related('tenant', 'instance').prefetch_related('vdus').all()
    serializer_class = VnfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


@method_decorator(name='list', decorator=swagger_decorators.vdu_list)
@method_decorator(name='retrieve', decorator=swagger_decorators.vdu_retrieve)
class VduViewSet(viewsets.ReadOnlyModelViewSet):
    """ VDU Resource """
    queryset = Vdu.objects.select_related('tenant', 'instance', 'vnf').all()
    serializer_class = VduSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


@method_decorator(name='retrieve', decorator=swagger_decorators.vnf_retrieve_by_uuid)
class VnfByUuid(generics.RetrieveAPIView):
    """Retrieve a VNF by its uuid."""
    queryset = Vnf.objects.select_related('instance', 'tenant').prefetch_related('vdus').all()
    serializer_class = VnfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = 'uuid'


@method_decorator(name='list', decorator=swagger_decorators.vnf_list_by_tenant_uuid)
@method_decorator(name='retrieve', decorator=swagger_decorators.vnf_retrieve_by_tenant_uuid)
class VnfsByTenant(viewsets.ReadOnlyModelViewSet):
    """List or Retrieve the VNFs of a specific tenant by its uuid."""
    serializer_class = VnfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Vnf.objects.select_related('instance', 'tenant').prefetch_related('vdus').all()
        if "tenant_uuid" in self.kwargs:
            queryset = queryset.filter(tenant__uuid=self.kwargs["tenant_uuid"])
        return queryset


@method_decorator(name='list', decorator=swagger_decorators.vnf_list_by_instance_uuid)
@method_decorator(name='retrieve', decorator=swagger_decorators.vnf_retrieve_by_instance_uuid)
class VnfsByInstance(viewsets.ReadOnlyModelViewSet):
    """List or Retrieve the VNFs of a specific network service instance by the instance's uuid."""
    serializer_class = VnfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Vnf.objects.select_related('instance', 'tenant').prefetch_related('vdus').all()
        if "instance_uuid" in self.kwargs:
            queryset = queryset.filter(instance__uuid=self.kwargs["instance_uuid"])
        return queryset


@method_decorator(name='retrieve', decorator=swagger_decorators.vdu_retrieve_by_uuid)
class VduByUuid(generics.RetrieveAPIView):
    """Retrieve a VDU by its UUID."""
    queryset = Vdu.objects.select_related('tenant', 'instance', 'vnf').all()
    serializer_class = VduSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = 'uuid'


@method_decorator(name='list', decorator=swagger_decorators.vdu_list_by_tenant_uuid)
@method_decorator(name='retrieve', decorator=swagger_decorators.vdu_retrieve_by_tenant_uuid)
class VdusByTenant(viewsets.ReadOnlyModelViewSet):
    """List or Retrieve the VDUs of a specific tenant by its UUID."""
    serializer_class = VduSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Vdu.objects.select_related('tenant', 'instance', 'vnf').all()
        if "tenant_uuid" in self.kwargs:
            queryset = queryset.filter(tenant__uuid=self.kwargs["tenant_uuid"])
        return queryset


@method_decorator(name='list', decorator=swagger_decorators.vdu_list_by_instance_uuid)
@method_decorator(name='retrieve', decorator=swagger_decorators.vdu_retrieve_by_instance_uuid)
class VdusByInstance(viewsets.ReadOnlyModelViewSet):
    """List or Retrieve the VDUs of a specific network service instance by the instance's UUID."""
    serializer_class = VduSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Vdu.objects.select_related('tenant', 'instance', 'vnf').all()
        if "instance_uuid" in self.kwargs:
            queryset = queryset.filter(instance__uuid=self.kwargs["instance_uuid"])
        return queryset


@method_decorator(name='list', decorator=swagger_decorators.instance_list_by_tenant_uuid)
@method_decorator(name='retrieve', decorator=swagger_decorators.instance_retrieve_by_tenant_uuid)
class InstanceByTenant(viewsets.ReadOnlyModelViewSet):
    """List or Retrieve the Network Service Instances by a Tenant's UUID."""
    serializer_class = InstanceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = Instance.objects.select_related('tenant').prefetch_related('vnfs', 'vdus').all()
        if "tenant_uuid" in self.kwargs:
            queryset = queryset.filter(tenant__uuid=self.kwargs["tenant_uuid"])
        return queryset


@method_decorator(name='retrieve', decorator=swagger_decorators.instance_retrieve_by_uuid)
class InstanceByUuid(generics.RetrieveAPIView):
    """Retrieve a NS Instance by its UUID."""
    queryset = Instance.objects.select_related('tenant').prefetch_related('vnfs', 'vdus').all()
    serializer_class = InstanceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = 'uuid'


@method_decorator(name='retrieve', decorator=swagger_decorators.tenant_retrieve_by_uuid)
class TenantByUuid(generics.RetrieveAPIView):
    """Retrieve a Tenant by its UUID."""
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    lookup_field = 'uuid'

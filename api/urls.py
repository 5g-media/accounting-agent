from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api import views
from accounting.settings import DEVELOPER_EMAIL

API_DESCRIPTION = """An API Built for the Accounting of the 5G-Media Project.

The `swagger-ui` view can be found [here](/api/v1/docs).  
The `ReDoc` view can be found [here](/api/v1/swagger.json).  
The swagger `YAML` document can be found [here](/api/v1/swagger.yaml).  
"""

schema_view = get_schema_view(
    openapi.Info(
        title="Accounting API",
        default_version='v1',
        description=API_DESCRIPTION,
        terms_of_service="",
        contact=openapi.Contact(email=DEVELOPER_EMAIL),
    ),
    validators=[],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_version = 'v1'

api_urlpatterns = [

    # Tenants
    url(r'^tenants$',
        views.TenantViewSet.as_view({'get': 'list'}),
        name='tenant-list'),
    url(r'^tenants/(?P<pk>[^/]+)$',
        views.TenantViewSet.as_view({'get': 'retrieve'}),
        name='tenant-detail'),
    url(r'^tenants/by-uuid/(?P<uuid>[^/]+)$',
        views.TenantByUuid.as_view(),
        name='tenant-detail'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/instances$',
        views.InstanceByTenant.as_view({'get': 'list'}),
        name='instance-list'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/instances/(?P<uuid>[^/]+)$',
        views.InstanceByTenant.as_view({'get': 'retrieve'}),
        name='instance-detail'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/vnfs$',
        views.VnfsByTenant.as_view({'get': 'list'}),
        name='vnf-list'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/vnfs/(?P<uuid>[^/]+)$',
        views.VnfsByTenant.as_view({'get': 'retrieve'}),
        name='vnf-detail'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/vdus$',
        views.VdusByTenant.as_view({'get': 'list'}),
        name='vdu-list'),
    url(r'^tenants/(?P<tenant_uuid>[^/]+)/vdus/(?P<uuid>[^/]+)$',
        views.VdusByTenant.as_view({'get': 'retrieve'}),
        name='vdu-detail'),

    # Network Service
    url(r'^instances$',
        views.InstanceViewSet.as_view({'get': 'list'}),
        name='instance-list'),
    url(r'^instances/(?P<pk>[^/]+)$',
        views.InstanceViewSet.as_view({'get': 'retrieve'}),
        name='instance-detail'),
    url(r'^instances/by-uuid/(?P<uuid>[^/]+)$',
        views.InstanceByUuid.as_view(),
        name='instance-detail'),
    url(r'^instances/(?P<instance_uuid>[^/]+)/vnfs$',
        views.VnfsByInstance.as_view({'get': 'list'}),
        name='vnf-list'),
    url(r'^instances/(?P<instance_uuid>[^/]+)/vnfs/(?P<uuid>[^/]+)$',
        views.VnfsByInstance.as_view({'get': 'retrieve'}),
        name='vnf-detail'),
    url(r'^instances/(?P<instance_uuid>[^/]+)/vdus$',
        views.VdusByInstance.as_view({'get': 'list'}),
        name='vdu-list'),
    url(r'^instances/(?P<instance_uuid>[^/]+)/vdus/(?P<uuid>[^/]+)$',
        views.VdusByInstance.as_view({'get': 'retrieve'}),
        name='vdu-detail'),
    url(r'^instances/by-tenant/(?P<tenant_uuid>[^/]+)$',
        views.InstanceByTenant.as_view({'get': 'list'}),
        name='instance-list'),
    url(r'^instances/by-tenant/(?P<tenant_uuid>[^/]+)/(?P<uuid>[^/]+)$',
        views.InstanceByTenant.as_view({'get': 'retrieve'}),
        name='instance-detail'),

    # Vnfs
    url(r'^vnfs$',
        views.VnfViewSet.as_view({'get': 'list'}),
        name='vnf-list'),
    url(r'^vnfs/(?P<pk>[^/]+)$',
        views.VnfViewSet.as_view({'get': 'retrieve'}),
        name='vnf-detail'),
    url(r'^vnfs/by-uuid/(?P<uuid>[^/]+)$',
        views.VnfByUuid.as_view(),
        name='vnf-detail'),
    url(r'^vnfs/by-tenant/(?P<tenant_uuid>[^/]+)$',
        views.VnfsByTenant.as_view({'get': 'list'}),
        name='vnf-list'),
    url(r'^vnfs/by-tenant/(?P<tenant_uuid>[^/]+)/(?P<uuid>[^/]+)$',
        views.VnfsByTenant.as_view({'get': 'retrieve'}),
        name='vnf-detail'),
    url(r'^vnfs/by-instance/(?P<instance_uuid>[^/]+)$',
        views.VnfsByInstance.as_view({'get': 'list'}),
        name='vnf-list'),
    url(r'^vnfs/by-instance/(?P<instance_uuid>[^/]+)/(?P<uuid>[^/]+)$',
        views.VnfsByInstance.as_view({'get': 'retrieve'}),
        name='vnf-detail'),

    # Vdus
    url(r'^vdus$',
        views.VduViewSet.as_view({'get': 'list'}),
        name='vdu-list'),
    url(r'^vdus/(?P<pk>[^/]+)$',
        views.VduViewSet.as_view({'get': 'retrieve'}),
        name='vdu-detail'),
    url(r'^vdus/by-uuid/(?P<uuid>[^/]+)$',
        views.VduByUuid.as_view(),
        name='vdu-detail'),
    url(r'^vdus/by-tenant/(?P<tenant_uuid>[^/]+)$',
        views.VdusByTenant.as_view({'get': 'list'}),
        name='vdu-list'),
    url(r'^vdus/by-tenant/(?P<tenant_uuid>[^/]+)/(?P<uuid>[^/]+)$',
        views.VdusByTenant.as_view({'get': 'retrieve'}),
        name='vdu-detail'),
    url(r'^vdus/by-instance/(?P<instance_uuid>[^/]+)$',
        views.VdusByInstance.as_view({'get': 'list'}),
        name='vdu-list'),
    url(r'^vdus/by-instance/(?P<instance_uuid>[^/]+)/(?P<uuid>[^/]+)$',
        views.VdusByInstance.as_view({'get': 'retrieve'}),
        name='vdu-detail'),

    # Documentation
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^docs/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]

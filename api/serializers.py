from rest_framework import serializers

from api.models import *


class InstanceSerializer(serializers.ModelSerializer):
    tenant_id = serializers.SlugRelatedField(
        source='tenant',
        read_only=True,
        slug_field='uuid'
    )
    vdu_ids = serializers.SlugRelatedField(
        source='vdus',
        many=True,
        read_only=True,
        slug_field="uuid"
    )
    vnf_ids = serializers.SlugRelatedField(
        source='vnfs',
        many=True,
        read_only=True,
        slug_field="uuid"
    )

    class Meta:
        model = Instance
        fields = ('id', 'uuid', 'ns_session_id', 'name', 'catalog_tenant', 'catalog_user', 'mano_id', 'mano_project',
                  'mano_user', 'nfvipop_id', 'state', 'created_at', 'tenant_id', 'vdu_ids', 'vnf_ids')


class VnfSerializer(serializers.HyperlinkedModelSerializer):
    tenant_id = serializers.SlugRelatedField(
        source='tenant',
        read_only=True,
        slug_field='uuid'
    )
    instance_id = serializers.SlugRelatedField(
        source='instance',
        read_only=True,
        slug_field='uuid'
    )
    vdu_ids = serializers.SlugRelatedField(
        source='vdus',
        many=True,
        read_only=True,
        slug_field="uuid"
    )

    class Meta:
        model = Vnf
        fields = ('id', 'uuid', 'name', 'vnf_session_id', 'tenant_id', 'instance_id', 'vdu_ids')


class VduSerializer(serializers.HyperlinkedModelSerializer):
    tenant_id = serializers.SlugRelatedField(
        source='tenant',
        read_only=True,
        slug_field='uuid'
    )
    instance_id = serializers.SlugRelatedField(
        source='instance',
        read_only=True,
        slug_field='uuid'
    )
    vnf_id = serializers.SlugRelatedField(
        source='instance',
        read_only=True,
        slug_field='uuid'
    )

    class Meta:
        model = Vdu
        fields = ('id', 'creation_date', 'tenant_id', 'instance_id', 'vnf_id',
                  'uuid', 'vdu_session_id', 'vcpu', 'vram', 'vdisk', 'state')


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    vdu_ids = serializers.SlugRelatedField(
        source='vdus',
        many=True,
        read_only=True,
        slug_field="uuid"
    )
    instance_ids = serializers.SlugRelatedField(
        source='instances',
        many=True,
        read_only=True,
        slug_field="uuid"
    )
    vnf_ids = serializers.SlugRelatedField(
        source='vnfs',
        many=True,
        read_only=True,
        slug_field="uuid"
    )

    class Meta:
        model = Tenant
        fields = ('id', 'uuid', 'description', 'name', 'created_at', 'instance_ids', 'vnf_ids', 'vdu_ids')

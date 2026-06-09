from rest_framework import serializers
from apps.clients.models import Client

class ClientSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'workspace_id',
            'created_by',
            'created_by_username',
            'name',
            'email',
            'phone',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'workspace_id', 'created_by', 'created_at', 'updated_at']

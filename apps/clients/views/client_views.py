from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.clients.models import Client
from apps.clients.serializers import ClientSerializer

class ClientListCreateAPIView(APIView):
    """
    List and Create clients under a specific workspace.
    """
    def get(self, request, workspace_id):
        # List active clients for this workspace
        clients = Client.objects.filter(workspace_id=workspace_id, is_active=True)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request, workspace_id):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically associate the workspace_id and the authenticated user
            client = serializer.save(workspace_id=workspace_id, created_by=request.user)
            return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetailAPIView(APIView):
    """
    Retrieve, update, and soft-delete a client.
    """
    def get_object(self, workspace_id, pk):
        return get_object_or_404(Client, workspace_id=workspace_id, pk=pk, is_active=True)

    def get(self, request, workspace_id, pk):
        client = self.get_object(workspace_id, pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, workspace_id, pk):
        client = self.get_object(workspace_id, pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, workspace_id, pk):
        client = self.get_object(workspace_id, pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workspace_id, pk):
        client = self.get_object(workspace_id, pk)
        # Perform soft-deletion as mandated by project rules
        client.is_active = False
        client.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

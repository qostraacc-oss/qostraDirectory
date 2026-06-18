import uuid
import jwt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from apps.clients.models import Client

User = get_user_model()


class ClientAPITests(APITestCase):
    def setUp(self):
        self.workspace_id = uuid.uuid4()
        self.user_id = str(uuid.uuid4())
        
        # Create a mock JWT token signed with settings.SECRET_KEY
        payload = {
            'user_id': self.user_id,
            'email': 'anfique@qostra.com',
            'first_name': 'Anfique',
            'last_name': 'Developer',
        }
        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_client_creation_and_user_sync(self):
        url = reverse('client-list-create', kwargs={'workspace_id': self.workspace_id})
        data = {
            'name': 'Acme Corp',
            'email': 'info@acme.com',
            'phone': '+1234567890',
        }
        
        # Before the request, the user should not exist in the local database
        self.assertFalse(User.objects.filter(id=self.user_id).exists())
        
        # POST request to create the client
        response = self.client.post(url, data, format='json')
        
        # Verify 201 Created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the user was synchronized automatically
        self.assertTrue(User.objects.filter(id=self.user_id).exists())
        user = User.objects.get(id=self.user_id)
        self.assertEqual(user.email, 'anfique@qostra.com')
        self.assertEqual(user.first_name, 'Anfique')
        
        # Verify the Client was created under the correct workspace and user
        self.assertEqual(Client.objects.count(), 1)
        client_obj = Client.objects.first()
        self.assertEqual(client_obj.name, 'Acme Corp')
        self.assertEqual(client_obj.workspace_id, self.workspace_id)
        self.assertEqual(client_obj.created_by, user)

    def test_client_crud_operations(self):
        url_list = reverse('client-list-create', kwargs={'workspace_id': self.workspace_id})
        
        # Create client
        response = self.client.post(url_list, {'name': 'Client 1'}, format='json')
        client_id = response.data['id']
        
        # Test List
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 1)
        
        # Test Detail Retrieve
        url_detail = reverse('client-detail', kwargs={'workspace_id': self.workspace_id, 'pk': client_id})
        response_detail = self.client.get(url_detail)
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data['name'], 'Client 1')
        
        # Test Update (PUT)
        response_update = self.client.put(url_detail, {'name': 'Client 1 Updated'}, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data['name'], 'Client 1 Updated')
        
        # Test Soft Delete
        response_delete = self.client.delete(url_detail)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it is soft-deleted (is_active=False, doesn't show in list by default)
        client_obj = Client.objects.get(id=client_id)
        self.assertFalse(client_obj.is_active)
        
        # Verify it does not appear in active client lists
        response_list_after = self.client.get(url_list)
        self.assertEqual(len(response_list_after.data), 0)

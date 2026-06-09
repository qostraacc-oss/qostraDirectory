from django.urls import path
from apps.clients.views import ClientListCreateAPIView, ClientDetailAPIView

urlpatterns = [
    path('', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('<uuid:pk>/', ClientDetailAPIView.as_view(), name='client-detail'),
]

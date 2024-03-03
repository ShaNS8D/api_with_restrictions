from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from adv.models import Adv
from adv.serializers import AdvSerializer
from adv.filters import AdvFilter
from adv.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

class AdvViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Adv.objects.all()
    serializer_class = AdvSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    filterset_class = AdvFilter    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOrReadOnly()]
        return []

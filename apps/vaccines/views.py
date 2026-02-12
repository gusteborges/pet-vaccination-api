from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vaccine
from .serializers import VaccineReadSerializer, VaccineWriteSerializer

class VaccineViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento do catálogo de vacinas.
    """
    queryset = Vaccine.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VaccineWriteSerializer
        return VaccineReadSerializer
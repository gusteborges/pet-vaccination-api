from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsStaffRole 
from .models import Vaccination
from .serializers import VaccinationReadSerializer, VaccinationWriteSerializer

class VaccinationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffRole]

    def get_queryset(self):
        return Vaccination.objects.select_related('pet', 'vaccine', 'applied_by').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VaccinationWriteSerializer
        return VaccinationReadSerializer
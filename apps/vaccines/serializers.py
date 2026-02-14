from rest_framework import serializers
from .models import Vaccine
from apps.vaccines.services import VaccineService

class VaccineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['name', 'description', 'required_doses', 'is_active']

    def validate_name(self, value):
        # Delega a limpeza para a service
        return VaccineService.normalize_name(value)

    def validate_required_doses(self, value):
        # Delega a validação de regra de negócio para a service
        try:
            return VaccineService.validate_required_doses(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
    

class VaccineReadSerializer(serializers.ModelSerializer):
    total_doses_administered = serializers.ReadOnlyField()

    class Meta:
        model = Vaccine
        fields = [
            'id', 'name', 'description', 'required_doses', 
            'is_active', 'created_at', 'updated_at', 'total_doses_administered'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_doses_administered']
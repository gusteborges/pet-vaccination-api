from rest_framework import serializers
from .models import Vaccine

class VaccineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['name', 'description', 'required_doses', 'is_active']

    # Validando que required_doses seja pelo menos 1
    def validate_required_doses(self, value):
        if value < 1:
            raise serializers.ValidationError("Required doses must be at least 1.")
        return value
    
    def validate_name(self, value):
        return value.strip()  # Remove espaços em branco extras
    

class VaccineReadSerializer(serializers.ModelSerializer):
    total_doses_administered = serializers.ReadOnlyField()

    class Meta:
        model = Vaccine
        fields = [
            'id', 'name', 'description', 'required_doses', 
            'is_active', 'created_at', 'updated_at', 'total_doses_administered'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_doses_administered']
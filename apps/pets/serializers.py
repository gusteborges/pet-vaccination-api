from rest_framework import serializers
from .models import Pet

from django.utils import timezone

class PetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'birth_date', 'rg_animal', 'tutor']

    # Este método deve estar fora da classe Meta
    def validate_birth_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value
    
class PetReadSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'birth_date', 'rg_animal', 'tutor', 'created_at']
        # Corrigido de ready_only_fields para read_only_fields
        read_only_fields = ['id', 'created_at']
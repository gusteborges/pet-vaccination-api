from rest_framework import serializers
from apps.pets.services import PetService
from .models import Pet

# Serializers para o modelo Pet
class PetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'birth_date', 'rg_animal', 'tutor']

    def validate_birth_date(self, value):
        try:
            return PetService.validate_birth_date(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
# O PetReadSerializer inclui o campo 'id' e 'created_at' para leitura, mas não para escrita.
class PetReadSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'birth_date', 'rg_animal', 'tutor', 'created_at']
        read_only_fields = ['id', 'created_at']
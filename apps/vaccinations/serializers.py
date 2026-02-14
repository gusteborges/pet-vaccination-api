from rest_framework import serializers
from .models import Vaccination
from apps.users.serializers import UserReadSerializer
from apps.pets.serializers import PetReadSerializer  
from apps.vaccines.serializers import VaccineReadSerializer 
from .services import VaccinationService, ValidationError


class VaccinationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ['pet', 'vaccine', 'application_date', 'dose_number']

    def validate(self, data):
        # Valida a sequência da dose e a cronologia das datas usando a service
        try:
            VaccinationService.validate_dose_sequence(
                data["pet"], 
                data["vaccine"], 
                data["dose_number"],
                data["application_date"] # Novo parâmetro enviado para a service
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message)
        
        return data
    
    #   Sobrescrevendo o método create para associar o usuário autenticado como o aplicador da vacina
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        return Vaccination.objects.create(applied_by=user, **validated_data)
        

class VaccinationReadSerializer(serializers.ModelSerializer):
    pet = PetReadSerializer(read_only=True)
    vaccine = VaccineReadSerializer(read_only=True)
    applied_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Vaccination
        fields = ['id', 'pet', 'vaccine', 'applied_by', 'application_date', 'dose_number', 'created_at']
        read_only_fields = fields
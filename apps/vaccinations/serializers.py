from rest_framework import serializers
from django.utils import timezone
from .models import Vaccination
from apps.pets.models import Pet
from apps.vaccines.models import Vaccine
from apps.users.serializers import UserReadSerializer
from apps.pets.serializers import PetReadSerializer  
from apps.vaccines.serializers import VaccineReadSerializer 


class VaccinationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ['pet', 'vaccine', 'application_date', 'dose_number'] 

    def validate_application_date(self, value): # Ajustado nome do método
        if value > timezone.now().date():
            raise serializers.ValidationError("A data de aplicação não pode ser no futuro.")
        return value
    
    # Validando que dose_number seja pelo menos 1
    def validate(self, data):
        pet = data["pet"]
        vaccine = data["vaccine"]
        dose_number = data["dose_number"]

        # Validando que dose_number não exceda o número de doses requeridas pela vacina
        if dose_number > vaccine.required_doses:
            raise serializers.ValidationError(
                f"This vaccine requires only {vaccine.required_doses} doses."
            )

        # Validando que a dose seja aplicada na ordem correta (dose 1, depois dose 2, etc.)
        last_dose = (
            Vaccination.objects
            .filter(pet=pet, vaccine=vaccine)
            .order_by("-dose_number")
            .first()
        )

        # Se já existe uma dose anterior, a próxima dose deve ser a seguinte (dose_number + 1)
        if last_dose:
            expected_next_dose = last_dose.dose_number + 1

            if dose_number != expected_next_dose:
                raise serializers.ValidationError(
                    f"Next dose must be {expected_next_dose}."
                )
        else: # Se não existe nenhuma dose anterior, a primeira dose deve ser 1
            if dose_number != 1:
                raise serializers.ValidationError(
                    "First dose must be 1."
                )

        return data
    
    #   Sobrescrevendo o método create para associar o usuário autenticado como o aplicador da vacina
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        # Ajuste para 'applied_by' conforme definido no seu modelo
        vaccination = Vaccination.objects.create(
            applied_by=user, 
            **validated_data
        )
        return vaccination
    

class VaccinationReadSerializer(serializers.ModelSerializer):
    pet = PetReadSerializer(read_only=True)
    vaccine = VaccineReadSerializer(read_only=True)

    class Meta:
        model = Vaccination
        fields = ['id', 'pet', 'vaccine', 'applied_by', 'application_date', 'dose_number', 'created_at']
        read_only_fields = fields
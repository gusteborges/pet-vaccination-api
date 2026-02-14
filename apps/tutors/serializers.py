from rest_framework import serializers

from apps.tutors.services import TutorService
from .models import Tutor

# Serializers para o modelo Tutor
class TutorWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['name', 'email', 'cpf', 'phone']

    # Validações personalizadas para CPF e email usando os métodos do TutorService
    # Metodo Simplificado para validar o CPF e email usando os métodos do TutorService. Se a validação falhar, uma ValidationError é levantada.
    def validate_cpf(self, value): 
        try:
            return TutorService.clean_cpf(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def validate_email(self, value):
        return TutorService.normalize_email(value)

# O TutorReaderSerializer inclui o campo 'id' e 'created_at' para leitura, mas não para escrita.
class TutorReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'name', 'email', 'cpf', 'phone', 'created_at']

        read_only_fields = ['id', 'created_at']  # Esses campos são somente leitura
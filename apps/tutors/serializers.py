from rest_framework import serializers
from .models import Tutor

# Serializers para o modelo Tutor
class TutorWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['name', 'email', 'cpf', 'phone']

    """
    Validando se o CPF tem exatamente 11 dígitos, ignorando quaisquer caracteres não numéricos.
    """
    def validate_cpf(self, value):
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 11:
            raise serializers.ValidationError("CPF must contain exactly 11 digits.")
        return digits # para garantir que o CPF seja armazenado apenas com os dígitos, sem formatação
    
    def validate_email(self, value):
        """
        Convertendo o email para minúsculas para garantir a consistência.
        Isso é útil para evitar problemas de case sensitivity ao comparar emails.
        """
        return value.lower()

# O TutorReaderSerializer inclui o campo 'id' e 'created_at' para leitura, mas não para escrita.
class TutorReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'name', 'email', 'cpf', 'phone', 'created_at']

        read_only_fields = ['id', 'created_at']  # Esses campos são somente leitura
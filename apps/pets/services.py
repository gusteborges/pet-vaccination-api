from django.utils import timezone
from django.core.exceptions import ValidationError

class PetService:
    @staticmethod
    def validate_birth_date(date_value):
        # Valida se a data de nascimento é coerente
        if date_value and date_value > timezone.now().date():
            raise ValidationError("A data de nascimento não pode ser no futuro.")
        return date_value
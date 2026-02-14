from django.core.exceptions import ValidationError

class VaccineService:
    @staticmethod
    def normalize_name(name):
        # Remove espaços extras do nome da vacina.
        return name.strip() if name else name

    @staticmethod
    def validate_required_doses(doses):
        # Garante que a vacina tenha pelo menos uma dose configurada.
        if doses < 1:
            raise ValidationError("A vacina deve exigir pelo menos 1 dose.")
        return doses
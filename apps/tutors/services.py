from django.core.exceptions import ValidationError

# Serviços relacionados ao modelo Tutor, como validação de CPF e normalização de email.
class TutorService:
    @staticmethod
    def clean_cpf(cpf_value):
        """Remove formatação e valida o tamanho do CPF."""
        digits = "".join(filter(str.isdigit, cpf_value))
        if len(digits) != 11:
            raise ValidationError("O CPF deve conter exatamente 11 dígitos.")
        return digits

    @staticmethod
    def normalize_email(email):
        return email.lower() if email else email
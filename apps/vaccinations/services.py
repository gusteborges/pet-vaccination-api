from django.core.exceptions import ValidationError
from .models import Vaccination

class VaccinationService:
    @staticmethod
    def validate_dose_sequence(pet, vaccine, dose_number, application_date):
        # 1. Procurar a última dose aplicada para este pet e vacina
        last_dose = (
            Vaccination.objects
            .filter(pet=pet, vaccine=vaccine)
            .order_by("-dose_number")
            .first()
        )

        if last_dose:
            # 2. Validar a sequência do número da dose
            expected_next_dose = last_dose.dose_number + 1
            if dose_number != expected_next_dose:
                raise ValidationError(f"A próxima dose deve ser a {expected_next_dose}.")
            
            # 3. Validar a cronologia das datas (A correção está aqui)
            if application_date <= last_dose.application_date:
                raise ValidationError(
                    f"A data da dose {dose_number} ({application_date}) não pode ser "
                    f"anterior ou igual à data da dose {last_dose.dose_number} ({last_dose.application_date})."
                )
                
        elif dose_number != 1:
            raise ValidationError("A primeira dose deve ser a de número 1.")
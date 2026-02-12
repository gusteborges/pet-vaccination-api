from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Vaccination(models.Model):

    pet = models.ForeignKey(
        "pets.Pet",
        on_delete=models.CASCADE,
        related_name="vaccinations"
    )

    vaccine = models.ForeignKey(
        "vaccines.Vaccine",
        on_delete=models.CASCADE,
        related_name="vaccinations"
    )

    applied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="applied_vaccinations"
    )

    dose_number = models.PositiveIntegerField()

    application_date = models.DateField()

    next_dose_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vaccination"
        verbose_name_plural = "Vaccinations"
        ordering = ["-application_date"]
        unique_together = ("pet", "vaccine", "dose_number")

    def clean(self):
        if self.pet.birth_date and self.application_date:
            if self.application_date < self.pet.birth_date:
                raise ValidationError(
                    "Application date cannot be before pet birth date."
                )

        if self.vaccine and self.dose_number:
            if self.dose_number > self.vaccine.required_doses:
                raise ValidationError(
                    f"This vaccine requires only {self.vaccine.required_doses} doses."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} (Dose {self.dose_number})"

from django.db import models
from core import settings

# Create your models here.
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

    created_at = models.DateTimeField(auto_now_add=True)
    next_dose_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Vaccination"
        verbose_name_plural = "Vaccinations"
        ordering = ["-application_date"]
        unique_together = ("pet", "vaccine", "dose_number")

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} (Dose {self.dose_number})"
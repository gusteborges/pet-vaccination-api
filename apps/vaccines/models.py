from django.db import models
from django.core.validators import MinValueValidator


class Vaccine(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        db_index=True
    )

    description = models.TextField(blank=True)

    required_doses = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vaccine"
        verbose_name_plural = "Vaccines"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def total_doses_administered(self):
        return self.vaccinations.count()

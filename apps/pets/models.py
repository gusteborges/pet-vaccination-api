from django.db import models


class Pet(models.Model):

    class Species(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        OTHER = "other", "Other"

    name = models.CharField(max_length=150)

    species = models.CharField(
        max_length=20,
        choices=Species.choices
    )

    breed = models.CharField(max_length=100, blank=True)

    birth_date = models.DateField(blank=True, null=True)

    rg_animal = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True
    )

    tutor = models.ForeignKey(
        "tutors.Tutor",
        on_delete=models.CASCADE,
        related_name="pets"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"

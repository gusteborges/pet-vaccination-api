from django.db import models

# Create your models here.
class Vaccine(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    required_doses = models.PositiveIntegerField() # 
    is_active = models.BooleanField(default=True) 
    total_doses_administered = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vaccine"
        verbose_name_plural = "Vaccines"
        ordering = ["name"]

    def __str__(self):
        return self.name
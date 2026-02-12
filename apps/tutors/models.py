from django.db import models

class Tutor(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutors"
        ordering = ["name"]

    def __str__(self):
        return self.name

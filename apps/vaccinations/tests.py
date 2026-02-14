from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.tutors.models import Tutor
from apps.pets.models import Pet
from apps.vaccines.models import Vaccine
from apps.vaccinations.models import Vaccination
from datetime import date, timedelta

User = get_user_model()

class VaccinationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='vet_user', 
            password='password123', 
            role='vet'
        )
        self.client.force_authenticate(user=self.user)
        
        self.tutor = Tutor.objects.create(name="Augusto", email="guste@email.com", cpf="12345678901")
        self.pet = Pet.objects.create(name="Rex", species="dog", tutor=self.tutor)
        # Vacina que requer 2 doses para testar a sequência
        self.vaccine = Vaccine.objects.create(name="V8", required_doses=2)
        
        self.url = reverse('vaccination-list')

    def test_create_first_dose_success(self):
        # Testa o registro da primeira dose com sucesso
        data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "dose_number": 1,
            "application_date": date.today() - timedelta(days=10)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_apply_second_dose_before_first_dose_date(self):
        # Garante que a dose 2 não pode ter uma data anterior ou igual à dose 1.
        
        # Cria a primeira dose manualmente no dia de hoje
        Vaccination.objects.create(
            pet=self.pet,
            vaccine=self.vaccine,
            dose_number=1,
            application_date=date.today(),
            applied_by=self.user
        )

        # Tenta aplicar a dose 2 com data de ONTEM
        data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "dose_number": 2,
            "application_date": date.today() - timedelta(days=1)
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("não pode ser anterior ou igual à data da dose 1", str(response.data))

    def test_must_follow_dose_sequence(self):
        # Garante que não se pode pular para a dose 2 sem a 1 existir.
        data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "dose_number": 2,
            "application_date": date.today()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
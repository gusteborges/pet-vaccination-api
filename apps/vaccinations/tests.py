from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.tutors.models import Tutor
from apps.pets.models import Pet
from apps.vaccines.models import Vaccine
from apps.vaccinations.models import Vaccination
from django.utils import timezone

User = get_user_model()

class VaccinationTests(APITestCase):
    def setUp(self):
        # Cria usuário Veterinário para autenticação
        self.user = User.objects.create_user(
            username='vet_user', 
            password='password123', 
            role='vet'
        )
        self.client.force_authenticate(user=self.user)
        
        # Cria dados básicos para os testes
        self.tutor = Tutor.objects.create(name="Augusto", email="guste@email.com", cpf="12345678901")
        self.pet = Pet.objects.create(name="Rex", species="dog", tutor=self.tutor)
        self.vaccine = Vaccine.objects.create(name="Antirrábica", required_doses=1)
        
        # Nome da rota gerada pelo DefaultRouter (basename='vaccination')
        self.url = reverse('vaccination-list')

    def test_create_vaccination_success(self):
        """Testa se um veterinário consegue registrar uma vacinação corretamente."""
        data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "dose_number": 1,
            "application_date": timezone.now().date()
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vaccination.objects.count(), 1)

    def test_applied_by_is_logged_user(self):
        """Verifica se o campo applied_by é preenchido automaticamente com o usuário logado."""
        data = {
            "pet": self.pet.id,
            "vaccine": self.vaccine.id,
            "dose_number": 1,
            "application_date": timezone.now().date()
        }
        response = self.client.post(self.url, data)
        vaccination = Vaccination.objects.first()
        self.assertEqual(vaccination.applied_by, self.user)
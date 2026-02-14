from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.tutors.models import Tutor
from django.contrib.auth import get_user_model

User = get_user_model()

class TutorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('tutor-list')

    def test_create_tutor_success(self):
        #Testa criação de tutor com CPF válido e email normalizado.
        data = {
            "name": "Augusto Borges",
            "email": "GUSTE@email.com",
            "cpf": "123.456.789-01",
            "phone": "3499999999"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica se a service normalizou o email e CPF
        tutor = Tutor.objects.get(name="Augusto Borges")
        self.assertEqual(tutor.email, "guste@email.com")
        self.assertEqual(tutor.cpf, "12345678901")

    def test_create_tutor_invalid_cpf(self):
        """Verifica erro ao enviar CPF com tamanho errado."""
        data = {"name": "Erro", "email": "e@e.com", "cpf": "123", "phone": "00"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
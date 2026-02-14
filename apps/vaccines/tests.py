from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class VaccineTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='staff', password='123', role='staff')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('vaccine-list')

    def test_create_vaccine_success(self):
        data = {
            "name": " V5  ", # Testando normalize_name service
            "description": "Vacina quíntupla",
            "required_doses": 3
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'V5') # Nome limpo pelo strip()

    def test_vaccine_min_doses(self):
        # Testa se a regra de negócio impede vacinas com 0 doses
        data = {"name": "Erro", "required_doses": 0}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
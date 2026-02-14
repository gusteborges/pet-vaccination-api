from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.tutors.models import Tutor
from datetime import date, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


class PetTests(APITestCase): 
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='123')
        self.client.force_authenticate(user=self.user)
        self.tutor = Tutor.objects.create(name="Tutor", email="t@t.com", cpf="11122233344")
        self.url = reverse('pet-list')

    # Teste para criação de pet com dados válidos
    def test_create_pet_success(self):
        data = {
            "name": "Rex",
            "species": "dog",
            "tutor": self.tutor.id,
            "birth_date": date.today() - timedelta(days=365)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pet_birth_date_future_fails(self):
        # Garante que a service bloqueia datas de nascimento futuras.
        data = {
            "name": "Rex",
            "species": "dog",
            "tutor": self.tutor.id,
            "birth_date": date.today() + timedelta(days=1)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
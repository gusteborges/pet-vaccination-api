from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='password123', role='admin'
        )
        self.staff_user = User.objects.create_user(
            username='staff', password='password123', role='staff'
        )
        self.url_list = reverse('user-list')
        self.url_me = reverse('user-me')

    def test_admin_can_create_user(self):
        # Verifica se um admin consegue criar novos usuários.
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "username": "novo_vet",
            "password": "secretpassword",
            "email": "vet@clinica.com",
            "role": "vet"
        }
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_cannot_create_user(self):
        # Verifica se usuários sem papel admin são bloqueados ao criar usuários
        self.client.force_authenticate(user=self.staff_user)
        data = {"username": "tentativa", "password": "123", "role": "admin"}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_own_profile_me(self):
        # Testa se o usuário autenticado consegue acessar seus próprios dados
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.url_me)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'staff')
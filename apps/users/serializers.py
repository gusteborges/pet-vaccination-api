from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.services import UserService


User = get_user_model()  # Importando o modelo User do Django

class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']

    def validate_email(self, value):
        return UserService.normalize_email(value)

    def create(self, validated_data):
        return UserService.create_user(validated_data)
    
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = fields
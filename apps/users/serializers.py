from rest_framework import serializers
from .models import User, get_user_model

User = get_user_model()  # Importando o modelo User do Django

class UserWriterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name','role']

    def validate_email(self, value):
        return value.lower()  # Convertendo o email para minúsculas para garantir a consistência

    # O método create é sobrescrito para garantir que a senha seja armazenada de forma segura (hashing).
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hashing da senha
        user.save()
        return user
    
class UserReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','role', 'created_at']
        read_only_fields = fields
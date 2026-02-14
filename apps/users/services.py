from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:
    @staticmethod
    def create_user(validated_data):
        # Encapsula a criação do usuário com hashing de senha.
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def normalize_email(email):
        # Garante consistência no formato do email.
        return email.lower() if email else email
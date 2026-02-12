from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

# Permissões personalizadas para controle de acesso baseado em papéis (roles) dos usuários.
class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role == 'admin' or request.user.is_superuser)
        )

# Permissão que permite acesso apenas a usuários com papel de Veterinário (Vet).
class IsVeterinarianRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == User.Role.VET
        )

# Permissão que permite acesso a usuários com papel de Staff, Veterinário ou Administrador.
class IsStaffRole(permissions.BasePermission):
    def has_permission(self, request, view):
        # Admins e Vets também possuem nível de acesso de Staff na hierarquia da clínica
        allowed_roles = [User.Role.ADMIN, User.Role.VET, User.Role.STAFF]
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role in allowed_roles or request.user.is_superuser)
        )

# Permissão que permite acesso a usuários com papel de Veterinário ou Administrador, mas apenas leitura para outros.
class IsVetOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.role in [User.Role.VET, User.Role.ADMIN] or request.user.is_superuser)
        )
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsAdminRole as IsAdmin
from .models import User
from .serializers import UserReadSerializer, UserWriteSerializer

# ViewSet para o modelo User, com ações personalizadas e controle de permissões.
class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.all()

    # Define serializers diferentes para leitura e escrita, garantindo que campos sensíveis sejam protegidos.
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserWriteSerializer
        # Retorna o serializer de leitura para as demais ações (list, retrieve, me)
        return UserReadSerializer

    # Define permissões diferentes para a ação "me" (acesso ao próprio perfil) e para as demais ações (admin).
    def get_permissions(self):
        if self.action == "me":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    # Ação personalizada para acessar o próprio perfil do usuário autenticado.
    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data)

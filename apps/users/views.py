from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsAdminRole as IsAdmin
from .models import User
from .serializers import UserWriteSerializer, UserWriteSerializer

# ViewSet para o modelo User, com ações personalizadas e controle de permissões.
class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserWriteSerializer
        return UserWriteSerializer

    def get_permissions(self):
        if self.action == "me":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserWriteSerializer(request.user)
        return Response(serializer.data)

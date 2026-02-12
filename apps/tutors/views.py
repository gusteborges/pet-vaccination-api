from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tutor
from .serializers import TutorWriterSerializer, TutorReaderSerializer

class TutorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] # Garante que apenas usuários autenticados possam acessar as rotas de tutor
    queryset = Tutor.objects.all()

    # O método get_serializer_class é sobrescrito para retornar o serializer correto com base na ação (create, update, partial_update para escrita e os demais para leitura).
    def get_queryset(self):
        return super().get_queryset()
    
    # O método get_serializer_class é sobrescrito para retornar o serializer correto com base na ação (create, update, partial_update para escrita e os demais para leitura).
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TutorWriterSerializer
        return TutorReaderSerializer
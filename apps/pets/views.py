from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Pet
from .serializers import PetReadSerializer, PetWriteSerializer

# ViewSet para o modelo Pet, utilizando diferentes serializers para leitura e escrita, e implementando filtros, busca e ordenação.
class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Filtros exatos
    filterset_fields = ["species", "tutor"]

    # Busca textual
    search_fields = ["name", "breed"]

    # Ordenação permitida
    ordering_fields = ["name", "birth_date", "created_at"]
    ordering = ["name"]

    # O método get_queryset é sobrescrito para otimizar as consultas usando select_related para o campo tutor, evitando consultas adicionais ao acessar os dados do tutor relacionados a cada pet.
    def get_queryset(self):
        return (
            Pet.objects
            .select_related("tutor")
        )

    # O método get_serializer_class é sobrescrito para retornar o serializer correto com base na ação (create, update, partial_update para escrita e os demais para leitura).
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PetWriteSerializer
        return PetReadSerializer
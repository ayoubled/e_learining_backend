from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models.niveau import Niveaux, Inscrit
from .niveau_serializers import NiveauxSerializer, InscritSerializer
from rest_framework.exceptions import ValidationError
from .models.formation import Formation

class NiveauxViewSet(viewsets.ModelViewSet):
    serializer_class = NiveauxSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Niveaux.objects.all()
        formation_id = self.request.query_params.get('formation_id')

        if formation_id:
            try:
                # Convert formation_id to integer
                formation_id = int(formation_id)
                queryset = queryset.filter(formation_id=formation_id)
            except ValueError:
                # Handle invalid integer format
                raise ValidationError({"formation_id": "Must be a valid integer."})
        
        return queryset


    def perform_create(self, serializer):
        serializer.save()


class InscritViewSet(viewsets.ModelViewSet):
    serializer_class = InscritSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        niveau_id = self.kwargs['niveau_pk']
        return Inscrit.objects.filter(niveau_id=niveau_id)

    def perform_create(self, serializer):
        niveau_id = self.kwargs['niveau_pk']
        serializer.save(niveau_id=niveau_id)
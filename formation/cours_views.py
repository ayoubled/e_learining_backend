# views.py 
from rest_framework import viewsets
from .models.cours import Cours
from .cour_serializers import CoursSerializer

class CoursViewSet(viewsets.ModelViewSet):
    serializer_class = CoursSerializer

    def get_queryset(self):
        niveau_pk = self.kwargs.get('niveau_pk')
        return Cours.objects.filter(niveau__pk=niveau_pk).order_by('ordre')

    def perform_create(self, serializer):
        niveau_pk = self.kwargs.get('niveau_pk')
        serializer.save(niveau_id=niveau_pk)
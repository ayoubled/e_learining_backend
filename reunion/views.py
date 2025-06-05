from rest_framework import viewsets, permissions
from .models import Reunion, ConcerneReunion, ParticiperReunion
from .serializers import ReunionSerializer, ConcerneReunionSerializer, ParticiperReunionSerializer

class IsFormateur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.utilisateur.type == 'formateur'

class ReunionViewSet(viewsets.ModelViewSet):
    serializer_class = ReunionSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormateur]

    def get_queryset(self):
        return Reunion.objects.filter(formateur=self.request.user.utilisateur)

    def perform_create(self, serializer):
        serializer.save(formateur=self.request.user.utilisateur)

class ConcerneReunionViewSet(viewsets.ModelViewSet):
    serializer_class = ConcerneReunionSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormateur]

    def get_queryset(self):
        return ConcerneReunion.objects.filter(
            reunion__formateur=self.request.user.utilisateur
        )

class ParticiperReunionViewSet(viewsets.ModelViewSet):
    serializer_class = ParticiperReunionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.utilisateur.type == 'formateur':
            return ParticiperReunion.objects.filter(
                reunion__formateur=self.request.user.utilisateur
            )
        return ParticiperReunion.objects.filter(etudiant=self.request.user.utilisateur)
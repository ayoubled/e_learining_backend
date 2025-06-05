# test/views_reponse.py
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models_reponse import (
    ReponseTestManuel,
    ReponseTestAuto,
    EvaluationResultTest
)
from .serializers_reponse import (
    ReponseTestManuelSerializer,
    ReponseTestAutoSerializer,
    EvaluationResultTestSerializer
)
from account.models import Etudiant  # Import Etudiant model

class ReponseTestManuelViewSet(viewsets.ModelViewSet):
    serializer_class = ReponseTestManuelSerializer
    permission_classes = []  # Remove authentication

    def get_queryset(self):
        # Get student ID from URL
        etudiant_id = self.kwargs['etudiant_id']
        return ReponseTestManuel.objects.filter(etudiant__pk=etudiant_id)

    def perform_create(self, serializer):
        try:
            # Get student or raise 404
            etudiant = Etudiant.objects.get(pk=self.kwargs['etudiant_id'])
            serializer.save(etudiant=etudiant)
            
        except Etudiant.DoesNotExist:
            raise serializers.ValidationError(
                {"error": f"Student with ID {self.kwargs['etudiant_id']} does not exist"}
            )

class ReponseTestAutoViewSet(viewsets.ModelViewSet):
    serializer_class = ReponseTestAutoSerializer
    permission_classes = []  # Remove authentication

    def get_queryset(self):
        etudiant_id = self.kwargs['etudiant_id']
        return ReponseTestAuto.objects.filter(etudiant__pk=etudiant_id)

    def perform_create(self, serializer):
        etudiant = Etudiant.objects.get(pk=self.kwargs['etudiant_id'])
        serializer.save(etudiant=etudiant)

class EvaluationResultTestViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationResultTestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only formateurs can access evaluations
        user = self.request.user.utilisateur
        if user.type != 'formateur':
            raise PermissionDenied("Only formateurs can access evaluations")
            
        return EvaluationResultTest.objects.filter(formateur=user.formateur)

    def perform_create(self, serializer):
        user = self.request.user.utilisateur
        if user.type != 'formateur':
            raise PermissionDenied("Only formateurs can create evaluations")
            
        serializer.save(formateur=user.formateur)
from rest_framework import serializers
from .models import Reunion, ConcerneReunion, ParticiperReunion
from account.models import Utilisateur
from formation.models.niveau import Niveaux
from django.utils import timezone

class ConcerneReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcerneReunion
        fields = ['id', 'reunion', 'niveau']

class ParticiperReunionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticiperReunion
        fields = ['id', 'reunion', 'etudiant']

class ReunionSerializer(serializers.ModelSerializer):
    formateur = serializers.PrimaryKeyRelatedField(read_only=True)
    niveaux = serializers.PrimaryKeyRelatedField(
        queryset=Niveaux.objects.all(),
        many=True,
        write_only=True
    )
    participants = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.filter(type='etudiant'),
        many=True,
        write_only=True,
        required=False
    )
    
    # Add read-only representations
    concerned_niveaux = serializers.SerializerMethodField(read_only=True)
    participating_students = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reunion
        fields = [
            'id_reunion', 'titre', 'date', 'formateur',
            'niveaux', 'participants',
            'concerned_niveaux', 'participating_students'
        ]

    def get_concerned_niveaux(self, obj):
        return obj.niveaux.values_list('id_niveau', flat=True)

    def get_participating_students(self, obj):
        return obj.participants.values_list('ID_Utilisateur', flat=True)

    def create(self, validated_data):
        niveaux = validated_data.pop('niveaux', [])
        participants = validated_data.pop('participants', [])
        
        reunion = Reunion.objects.create(**validated_data)
        
        # Create through-model entries
        for niveau in niveaux:
            ConcerneReunion.objects.create(reunion=reunion, niveau=niveau)
            
        for etudiant in participants:
            ParticiperReunion.objects.create(reunion=reunion, etudiant=etudiant)
            
        return reunion
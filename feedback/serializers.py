from rest_framework import serializers
from .models import Feedback
from formation.serializers import FormationSerializer
from formation.models.formation import Formation
from account.models import Etudiant , Formateur


class FeedbackSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id_feedback', 'contenu', 'date', 'note_sur_5',
            'etudiant', 'formateur', 'user_info', 
            'gerant_reponse', 'date_reponse'
        ]
        read_only_fields = ['id_feedback', 'date', 'date_reponse']

    def get_user_info(self, obj):
        if obj.etudiant:
            return {
                'type': 'etudiant',
                'id': obj.etudiant.ID_Utilisateur_id,
                'nom': obj.etudiant.ID_Utilisateur.Nom,
                'prenom': obj.etudiant.ID_Utilisateur.Prenom
            }
        elif obj.formateur:  
            return {
                'type': 'formateur',
                'id': obj.formateur.ID_Utilisateur_id,
                'nom': obj.formateur.ID_Utilisateur.Nom,
                'prenom': obj.formateur.ID_Utilisateur.Prenom
            }
        return None  

    def validate(self, data):
        if not data.get('etudiant') and not data.get('formateur'):
            raise serializers.ValidationError(
                "Either student or formateur must be provided"
            )
        return data
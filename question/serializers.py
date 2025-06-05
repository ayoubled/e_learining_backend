from rest_framework import serializers
from .models import Question
from account.models import Utilisateur
from formation.models.niveau import Niveaux

class QuestionSerializer(serializers.ModelSerializer):
    etudiant = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.filter(type='etudiant'),
        required=False
    )
    formateur = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    niveau = serializers.PrimaryKeyRelatedField(
        queryset=Niveaux.objects.all(),
        pk_field=serializers.IntegerField(source='id_niveau')
    )

    class Meta:
        model = Question
        fields = [
            'id_question', 'description', 'reponse',
            'etudiant', 'formateur', 'niveau', 'date_creation'
        ]
        read_only_fields = ['id_question', 'date_creation', 'formateur', 'reponse']

    def validate(self, data):
        if self.context['request'].user.utilisateur.type == 'etudiant':
            if 'reponse' in data or 'formateur' in data:
                raise serializers.ValidationError("Students can only ask questions")
        return data
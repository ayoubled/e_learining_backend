from rest_framework import serializers
from .models_reponse import (
    ReponseTestManuel,
    ReponseTestAuto,
    EvaluationResultTest
)
from .models import ChoixTest

class ReponseTestManuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReponseTestManuel
        fields = ['etudiant', 'question', 'reponse']
        extra_kwargs = {'etudiant': {'read_only': True}}

class ReponseTestAutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReponseTestAuto
        fields = ['etudiant', 'question', 'reponse']
        extra_kwargs = {
            'etudiant': {'read_only': True},
            'reponse': {'queryset': ChoixTest.objects.all()}
        }

class EvaluationResultTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationResultTest
        fields = ['reponse', 'formateur', 'note']
        extra_kwargs = {'formateur': {'read_only': True}}
from rest_framework import serializers
from .models.niveau import Niveaux, Inscrit
from formation.models.formation import Formation
class NiveauxSerializer(serializers.ModelSerializer):
    formation = serializers.PrimaryKeyRelatedField(queryset=Formation.objects.all())
    
    class Meta:
        model = Niveaux
        fields = ['id_niveau', 'description', 'ordre', 'formation']
        read_only_fields = ['id_niveau']  
        extra_kwargs = {
            'ordre': {'min_value': 0}
        }

class InscritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrit
        fields = ['id', 'niveau', 'etudiant', 'date_inscription', 'paye']
        read_only_fields = ['niveau', 'date_inscription']  
        extra_kwargs = {
            'etudiant': {'required': True}
        }

    def validate(self, data):
        # Get niveau from URL parameters instead of request data
        niveau_id = self.context['view'].kwargs['niveau_pk']
        data['niveau'] = Niveaux.objects.get(pk=niveau_id)
        
        if Inscrit.objects.filter(niveau=data['niveau'], etudiant=data['etudiant']).exists():
            raise serializers.ValidationError("Student already enrolled in this level")
        return data
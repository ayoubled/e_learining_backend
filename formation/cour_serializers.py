from rest_framework import serializers
from .models.cours import Cours

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = [
            'ID_Cours', 
            'Titre', 
            'Description', 
            'Duree', 
            'Type', 
            'url', 
            'ordre', 
            'niveau'
        ]
        extra_kwargs = {
            'niveau': {'read_only': True}
        }
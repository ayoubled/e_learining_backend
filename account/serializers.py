from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Compte, Utilisateur, Etudiant, Gerant, Formateur
from django.db import IntegrityError
from .models import PointInterest, Diplome

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    Nom = serializers.CharField()
    Prenom = serializers.CharField()
    Date_naissance = serializers.DateField()
    Telephone = serializers.CharField()
    Sexe = serializers.CharField()
    type = serializers.CharField()
    
    # Optional fields
    speciality = serializers.CharField(required=False)
    Domaine_expertise = serializers.CharField(required=False)
    Experience_annees = serializers.IntegerField(required=False)

    def validate_email(self, value):
        """
        Validate email uniqueness
        """
        if Compte.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        try:
            
            compte = Compte.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password']
            )
            
            
            utilisateur = Utilisateur.objects.create(
                Nom=validated_data['Nom'],
                Prenom=validated_data['Prenom'],
                Date_naissance=validated_data['Date_naissance'],
                Telephone=validated_data['Telephone'],
                Sexe=validated_data['Sexe'],
                type=validated_data['type']
            )
            
            
            compte.utilisateur = utilisateur
            compte.save()
            
            
            user_type = validated_data['type']
            if user_type == 'etudiant':
                Etudiant.objects.create(
                    ID_Utilisateur=utilisateur,
                    speciality=validated_data.get('speciality', '')
                )
            elif user_type == 'formateur':
                Formateur.objects.create(
                    ID_Utilisateur=utilisateur,
                    Domaine_expertise=validated_data.get('Domaine_expertise', ''),
                    Experience_annees=validated_data.get('Experience_annees', 0)
                )
            elif user_type == 'gerant':
                Gerant.objects.create(ID_Utilisateur=utilisateur)

            return compte

        except IntegrityError as e:
            if 'email' in str(e).lower():
                raise serializers.ValidationError(
                    {"email": ["This email address is already in use."]}
                )
            raise serializers.ValidationError({"error": ["Registration failed. Please try again."]})

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'status': 'Registration successful'
        }

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['type'] = self.user.utilisateur.type
        
        data['id_utilisateur'] = self.user.utilisateur.ID_Utilisateur
        return data

class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}





class PointInterestSerializer(serializers.ModelSerializer):
    etudiant = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="Student ID (auto-assigned)"
    )

    class Meta:
        model = PointInterest
        fields = ['ID_point_interest', 'point_interest', 'etudiant']
        read_only_fields = ['ID_point_interest', 'etudiant']

    def validate(self, data):
        if self.context['request'].user.utilisateur.type != 'etudiant':
            raise serializers.ValidationError("Only students can create interest points")
        return data

class DiplomeSerializer(serializers.ModelSerializer):
    formateur = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="Formateur ID (auto-assigned)"
    )

    class Meta:
        model = Diplome
        fields = ['ID_Diplome', 'url', 'formateur']
        read_only_fields = ['ID_Diplome', 'formateur']

    def validate(self, data):
        if self.context['request'].user.utilisateur.type != 'formateur':
            raise serializers.ValidationError("Only formateurs can add diplomas")
        return data
class UserProfileSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    speciality = serializers.CharField(required=False)
    Domaine_expertise = serializers.CharField(required=False)
    Experience_annees = serializers.IntegerField(required=False)

    class Meta:
        model = Utilisateur
        fields = [
            'ID_Utilisateur', 'Nom', 'Prenom', 'Date_naissance',
            'Telephone', 'Sexe', 'type', 'speciality',
            'Domaine_expertise', 'Experience_annees'
        ]
        read_only_fields = ['ID_Utilisateur']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add role-specific fields
        if instance.type == 'etudiant' and hasattr(instance, 'etudiant'):
            data['speciality'] = instance.etudiant.speciality
        elif instance.type == 'formateur' and hasattr(instance, 'formateur'):
            data['Domaine_expertise'] = instance.formateur.Domaine_expertise
            data['Experience_annees'] = instance.formateur.Experience_annees
        return data

    def update(self, instance, validated_data):
        # Update common fields
        instance.Nom = validated_data.get('Nom', instance.Nom)
        instance.Prenom = validated_data.get('Prenom', instance.Prenom)
        instance.Date_naissance = validated_data.get('Date_naissance', instance.Date_naissance)
        instance.Telephone = validated_data.get('Telephone', instance.Telephone)
        instance.Sexe = validated_data.get('Sexe', instance.Sexe)
        instance.save()

        # Update role-specific fields
        if instance.type == 'etudiant':
            etudiant = instance.etudiant
            etudiant.speciality = validated_data.get('speciality', etudiant.speciality)
            etudiant.save()
        elif instance.type == 'formateur':
            formateur = instance.formateur
            formateur.Domaine_expertise = validated_data.get('Domaine_expertise', formateur.Domaine_expertise)
            formateur.Experience_annees = validated_data.get('Experience_annees', formateur.Experience_annees)
            formateur.save()

        return instance
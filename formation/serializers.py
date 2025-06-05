from formation.cour_serializers import CoursSerializer
from formation.models.niveau import Niveaux
from quiz.serializers import QuizSerializer
from rest_framework import serializers
from examen.serializers import ExamSerializer 
from test.models import QuestionTest, Test
from account.models import Formateur
from test.serializers import ChoixTestSerializer
from .models.formation import Formation, MoteCles, Requirement, presiser

class MoteClesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoteCles
        fields = ['id_mote_cles', 'type', 'description']
        read_only_fields = ['id_mote_cles']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id_requirements', 'description', 'ordre']
        read_only_fields = ['id_requirements']

class FormationSerializer(serializers.ModelSerializer):
    mote_cles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MoteCles.objects.all(),
        required=False
    )
    formateur = serializers.PrimaryKeyRelatedField(
        queryset=Formateur.objects.all(),
        required=True
    )
    prerequis = RequirementSerializer(many=True, required=False)
    formateur = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Formation
        fields = [
            'id_formation', 'titre', 'description', 'categorie',
            'formateur', 'mote_cles', 'prerequis'
        ]
        read_only_fields = ['id_formation']

    def create(self, validated_data):
        mote_cles = validated_data.pop('mote_cles', [])
        prerequis_data = validated_data.pop('prerequis', [])
        
        # Create formation
        formation = Formation.objects.create(**validated_data)
        
        # Create MoteCles relationships
        for mc in mote_cles:
            presiser.objects.create(formation=formation, mot_cle=mc)
        
        # Create Requirements
        for req_data in prerequis_data:
            Requirement.objects.create(formation=formation, **req_data)
            
        return formation

    def update(self, instance, validated_data):
        mote_cles = validated_data.pop('mote_cles', None)
        prerequis_data = validated_data.pop('prerequis', None)
        
        # Update main fields
        instance = super().update(instance, validated_data)
        
        # Update MoteCles relationships
        if mote_cles is not None:
            # Clear existing relationships
            instance.presiser_set.all().delete()
            # Create new relationships
            for mc in mote_cles:
                presiser.objects.create(formation=instance, mot_cle=mc)
        
        # Update Requirements
        if prerequis_data is not None:
            # Clear existing requirements
            instance.prerequis.all().delete()
            # Create new requirements
            for req_data in prerequis_data:
                Requirement.objects.create(formation=instance, **req_data)
        
        return instance

class FormationDetailSerializer(FormationSerializer):
    mote_cles = MoteClesSerializer(many=True, read_only=True)
    prerequis = RequirementSerializer(many=True, read_only=True)



class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['ID_Test', 'Description','questions']


class QuestionTestSerializer(serializers.ModelSerializer):
    auto_correction = serializers.SerializerMethodField()
    manual_correction = serializers.SerializerMethodField()

    class Meta:
        model = QuestionTest
        fields = ['ID_QuestionTest', 'description', 'type', 'auto_correction', 'manual_correction']

    def get_auto_correction(self, obj):
        if hasattr(obj, 'auto_correction'):
            return {
                'note_question': obj.auto_correction.note_question,
                'choix': ChoixTestSerializer(obj.auto_correction.choix.all(), many=True).data
            }
        return None

    def get_manual_correction(self, obj):
        if hasattr(obj, 'manual_correction'):
            return {'exists': True}  # Customize as needed
        return None
class NiveauxSerializer(serializers.ModelSerializer):
    cours = CoursSerializer(many=True, read_only=True)
    quiz = QuizSerializer(many=True, read_only=True)
    exams = ExamSerializer(many=True, read_only=True)  
    
    class Meta:
        model = Niveaux
        fields = ['id_niveau', 'description', 'ordre', 'cours', 'quiz', 'exams']



class FormationFullSerializer(serializers.ModelSerializer):
    niveaux = NiveauxSerializer(many=True, read_only=True)
    mote_cles = MoteClesSerializer(many=True, read_only=True)
    prerequis = RequirementSerializer(many=True, read_only=True)
    tests = TestSerializer(many=True, read_only=True)  # Add tests
    
    class Meta:
        model = Formation
        fields = [
            'id_formation', 'titre', 'description', 'categorie',
            'formateur', 'mote_cles', 'prerequis', 'niveaux', 'tests'
        ]
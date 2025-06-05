# examen/serializers.py
from rest_framework import serializers
from account.models import Etudiant, Formateur
from .models import (
    Exam,
    QuestionExam,
    AutoCorrectionExam,
    ManuelCorrectionExam,
    ChoixExam,
    ReponseExamAuto,
    ReponseExamManuel,
    EvaluationResultExam
)


class AutoCorrectionExamSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionExam.objects.filter(type='auto'),
        required=True
    )

    class Meta:
        model = AutoCorrectionExam
        fields = ['question', 'note']

class ManuelCorrectionExamSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionExam.objects.filter(type='manuel'),
        required=True
    )

    class Meta:
        model = ManuelCorrectionExam
        fields = ['question']


class QuestionExamSerializer(serializers.ModelSerializer):
    auto_correction = AutoCorrectionExamSerializer(read_only=True)
    manual_correction = ManuelCorrectionExamSerializer(read_only=True)
    
    class Meta:
        model = QuestionExam
        fields = [
            'id_question_exam',
            'contenu',
            'type',
            'exam',
            'auto_correction',
            'manual_correction'
        ]
        read_only_fields = ('id_question_exam', 'exam')

    def validate_type(self, value):
        if self.instance and self.instance.type != value:
            raise serializers.ValidationError("Question type cannot be changed after creation")
        return value


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id_exam', 'evaluation_state', 'niveau']
        read_only_fields = ('id_exam',)


class ChoixExamSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        queryset=QuestionExam.objects.filter(type='auto'),
        required=True
    )

    class Meta:
        model = ChoixExam
        fields = ['id_choix_exam', 'description', 'est_correct', 'question']
        read_only_fields = ('id_choix_exam',)

class ReponseExamAutoSerializer(serializers.ModelSerializer):
    etudiant = serializers.PrimaryKeyRelatedField(
        queryset=Etudiant.objects.all(),
        required=True
    )

    class Meta:
        model = ReponseExamAuto
        fields = ['etudiant', 'question', 'choix', 'date_passer_exam']
        read_only_fields = ('date_passer_exam',)

    def validate(self, data):
        user = self.context['request'].user
        etudiant = data['etudiant']
        # Existing validation
        question = data['question']
        if question.type != 'auto':
            raise serializers.ValidationError("This question requires auto-correction")
        
        if not hasattr(question, 'auto_correction'):
            raise serializers.ValidationError("Auto correction not configured")
            
        return data


class ReponseExamManuelSerializer(serializers.ModelSerializer):
    etudiant = serializers.PrimaryKeyRelatedField(
        queryset=Etudiant.objects.all(),
        required=True
    )

    class Meta:
        model = ReponseExamManuel
        fields = ['etudiant', 'question', 'reponse', 'date_passer_exam']
        read_only_fields = ('date_passer_exam',)

    def validate(self, data):
        user = self.context['request'].user
        etudiant = data['etudiant']
        question = data['question']
        if question.type != 'manuel':
            raise serializers.ValidationError("This question requires manual evaluation")
            
        return data


class EvaluationResultExamSerializer(serializers.ModelSerializer):
    formateur = serializers.PrimaryKeyRelatedField(
        queryset=Formateur.objects.all(),
        required=True
    )

    class Meta:
        model = EvaluationResultExam
        fields = ['reponse', 'formateur', 'note', 'date_evaluation']
        read_only_fields = ('date_evaluation',)

    def validate(self, data):
        user = self.context['request'].user
        # Validate response belongs to a manual question
        if data['reponse'].question.type != 'manuel':
            raise serializers.ValidationError("Can only evaluate manual questions")
            
        return data




class ChoixExamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoixExam
        fields = ['description', 'est_correct']

class QuestionExamSerializer(serializers.ModelSerializer):
    auto_correction = AutoCorrectionExamSerializer(read_only=True)
    manual_correction = ManuelCorrectionExamSerializer(read_only=True)
    choix = ChoixExamWriteSerializer(many=True, required=False)
    exam = serializers.PrimaryKeyRelatedField(  # Changed to writable field
        queryset=Exam.objects.all(),
        required=True
    )

    class Meta:
        model = QuestionExam
        fields = [
            'id_question_exam',
            'contenu',
            'type',
            'exam',  # Now included in request body
            'auto_correction',
            'manual_correction',
            'choix'
        ]
        read_only_fields = ('id_question_exam',)

    def validate(self, data):
        if self.instance and self.instance.type != data.get('type', self.instance.type):
            raise serializers.ValidationError("Question type cannot be changed after creation")
        
        question_type = data.get('type')
        choix_data = data.get('choix', [])

        if question_type == 'auto':
            if not choix_data:
                raise serializers.ValidationError({"choix": "At least one choice is required for auto-type questions."})
            if not any(choice.get('est_correct', False) for choice in choix_data):
                raise serializers.ValidationError({"choix": "At least one choice must be correct."})
        elif question_type == 'manuel' and choix_data:
            raise serializers.ValidationError({"choix": "Choices are not allowed for manual-type questions."})

        return data

    def create(self, validated_data):
        choix_data = validated_data.pop('choix', [])
        question = super().create(validated_data)
        
        if question.type == 'auto':
            for choix in choix_data:
                ChoixExam.objects.create(question=question, **choix)
        
        return question
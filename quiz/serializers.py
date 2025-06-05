from formation.models.niveau import Niveaux
from rest_framework import serializers
from .models import Quiz, QuestionQuiz, ChoixQuiz, ReponseQuiz
from account.models import Etudiant

class QuizSerializer(serializers.ModelSerializer):
    niveau = serializers.PrimaryKeyRelatedField(
        queryset=Niveaux.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Quiz
        fields = ['ID_Quiz', 'titre', 'niveau', 'date_creation']
        read_only_fields = ['ID_Quiz', 'date_creation']
class ChoixQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoixQuiz
        fields = ['ID_Choix_Quiz', 'contenu', 'est_correct']

class QuestionQuizSerializer(serializers.ModelSerializer):
    choix = ChoixQuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuestionQuiz
        fields = ['ID_QuestionQuiz', 'contenu', 'ordre', 'choix']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionQuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['ID_Quiz', 'niveau', 'date_creation', 'questions']

class ReponseQuizSerializer(serializers.ModelSerializer):
    etudiant = serializers.PrimaryKeyRelatedField(queryset=Etudiant.objects.all())  
    question = serializers.PrimaryKeyRelatedField(queryset=QuestionQuiz.objects.all())
    reponse = serializers.PrimaryKeyRelatedField(queryset=ChoixQuiz.objects.all())

    class Meta:
        model = ReponseQuiz
        fields = ['etudiant', 'question', 'reponse']  


class QuestionQuizSerializer(serializers.ModelSerializer):
    niveau_id = serializers.IntegerField(write_only=True)
    quiz_id = serializers.IntegerField(write_only=True)
    choix = ChoixQuizSerializer(many=True)

    class Meta:
        model = QuestionQuiz
        fields = ['ID_QuestionQuiz', 'contenu', 'ordre', 'niveau_id', 'quiz_id', 'choix']
        read_only_fields = ['ID_QuestionQuiz']

    def validate(self, data):
        # Verify niveau exists
        niveau_id = data.get('niveau_id')
        quiz_id = data.get('quiz_id')
        
        if not Niveaux.objects.filter(id_niveau=niveau_id).exists():
            raise serializers.ValidationError("Niveau introuvable")
            
        if not Quiz.objects.filter(ID_Quiz=quiz_id, niveau_id=niveau_id).exists():
            raise serializers.ValidationError("Quiz introuvable dans ce niveau")
            
        return data

    def create(self, validated_data):
        niveau_id = validated_data.pop('niveau_id')
        quiz_id = validated_data.pop('quiz_id')
        choix_data = validated_data.pop('choix')
        
        try:
            quiz = Quiz.objects.get(ID_Quiz=quiz_id, niveau_id=niveau_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Combinaison niveau/quiz invalide")

        question = QuestionQuiz.objects.create(
            quiz=quiz,
            **validated_data
        )
        
        # Create choices
        for choix in choix_data:
            ChoixQuiz.objects.create(question=question, **choix)
            
        return question
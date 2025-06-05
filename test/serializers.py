from rest_framework import serializers
from .models import Test, QuestionTest, ChoixTest, AutoCorrectionTest
from formation.models.formation import Formation
class ChoixTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoixTest
        fields = ['ID_ChoixTest', 'description', 'Est_correct']
        read_only_fields = ['ID_ChoixTest']

class QuestionTestSerializer(serializers.ModelSerializer):
    test = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(),
        required=True,
        error_messages={'required': 'test ID is required'}
    )
    choix = ChoixTestSerializer(
        many=True,
        source='auto_correction.choix',
        read_only=True
    )

    class Meta:
        model = QuestionTest
        fields = ['ID_QuestionTest', 'description', 'type', 'test', 'choix']
        read_only_fields = ['ID_QuestionTest']

    def create(self, validated_data):
        # Extract choices data from request
        choix_data = self.context['request'].data.get('choix', [])
        
        # Create question first
        question = QuestionTest.objects.create(**validated_data)
        
        # Create choices if auto-type
        if question.type == 'auto':
            for choix in choix_data:
                ChoixTest.objects.create(
                    question=question.auto_correction,
                    description=choix.get('description'),
                    Est_correct=choix.get('Est_correct', False)
                )
        
        return question
    

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionTestSerializer(many=True, read_only=True)
    formation = serializers.PrimaryKeyRelatedField(
        queryset=Formation.objects.all(),
        required=True,
        error_messages={'required': 'formation ID is required'}
    )

    class Meta:
        model = Test
        fields = ['ID_Test', 'Description', 'formation', 'questions']
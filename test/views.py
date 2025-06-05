from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Test, QuestionTest, ChoixTest,AutoCorrectionTest
from .serializers import TestSerializer, QuestionTestSerializer, ChoixTestSerializer

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

    def create(self, request, *args, **kwargs):
        if 'formation' not in request.data:
            return Response(
                {"error": "formation ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class QuestionTestViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionTestSerializer
    queryset = QuestionTest.objects.all()
    
    # Remove conflicting get_queryset filter
    def get_queryset(self):
        return super().get_queryset()

class ChoixTestViewSet(viewsets.ModelViewSet):
    serializer_class = ChoixTestSerializer
    
    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return ChoixTest.objects.filter(
            question__question__ID_QuestionTest=question_id
        )

    def perform_create(self, serializer):
        question_id = self.kwargs['question_id']
        try:
            # Verify question exists and is auto type
            question = QuestionTest.objects.get(ID_QuestionTest=question_id)
            auto_correction = AutoCorrectionTest.objects.get(question=question)
            serializer.save(question=auto_correction)
        except QuestionTest.DoesNotExist:
            return Response(
                {"error": "Question not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except AutoCorrectionTest.DoesNotExist:
            return Response(
                {"error": "Question must be auto-correct type"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
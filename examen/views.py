# examen/views.py
from rest_framework import generics, permissions,serializers
from django.shortcuts import get_object_or_404
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
from .serializers import (
    ExamSerializer,
    QuestionExamSerializer,
    AutoCorrectionExamSerializer,
    ManuelCorrectionExamSerializer,
    ChoixExamSerializer,
    ReponseExamAutoSerializer,
    ReponseExamManuelSerializer,
    EvaluationResultExamSerializer
)

# Exam Views
class ExamListCreate(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

# Question Views
class QuestionExamListCreate(generics.ListCreateAPIView):
    serializer_class = QuestionExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = QuestionExam.objects.all()

class QuestionExamDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        exam_id = self.kwargs['exam_id']
        return QuestionExam.objects.filter(exam__id_exam=exam_id)

# Correction Views
class AutoCorrectionExamCreate(generics.CreateAPIView):
    serializer_class = AutoCorrectionExamSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        if question.type != 'auto':
            raise serializers.ValidationError("Can only add auto-correction to auto-type questions")
        serializer.save()

class ManuelCorrectionExamCreate(generics.CreateAPIView):
    serializer_class = ManuelCorrectionExamSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        if question.type != 'manuel':
            raise serializers.ValidationError("Can only add manual correction to manual-type questions")
        serializer.save()

# Choice Views
class ChoixExamListCreate(generics.ListCreateAPIView):
    serializer_class = ChoixExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        question_id = self.request.data.get('question')
        return ChoixExam.objects.filter(question__id_question_exam=question_id)

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        if question.type != 'auto':
            raise serializers.ValidationError("Choices can only be added to auto-type questions")
        serializer.save()

# Response Views
class StudentResponseAutoCreate(generics.CreateAPIView):
    serializer_class = ReponseExamAutoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not (hasattr(request.user.utilisateur, 'etudiant') or request.user.is_staff):
            self.permission_denied(
                request,
                message="Students can only submit for themselves, admins for others",
                code=403
            )

class StudentResponseManuelCreate(generics.CreateAPIView):
    serializer_class = ReponseExamManuelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not (hasattr(request.user.utilisateur, 'etudiant') or request.user.is_staff):
            self.permission_denied(
                request,
                message="Students can only submit for themselves, admins for others",
                code=403
            )

# Evaluation Views
class EvaluationResultCreate(generics.CreateAPIView):
    serializer_class = EvaluationResultExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if not (hasattr(request.user.utilisateur, 'formateur') or request.user.is_staff):
            self.permission_denied(
                request,
                message="Only formateurs can submit evaluations",
                code=403
            )
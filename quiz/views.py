
from rest_framework import viewsets, status,serializers
from django.shortcuts import get_object_or_404 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Quiz, QuestionQuiz, ChoixQuiz, ReponseQuiz
from .serializers import QuizSerializer, QuestionQuizSerializer, ReponseQuizSerializer,ChoixQuizSerializer

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "Quiz créé avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": "Données invalides",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class QuestionQuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionQuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_pk')
        return QuestionQuiz.objects.filter(quiz_id=quiz_id)

    def create(self, request, *args, **kwargs):
        try:
            quiz = Quiz.objects.get(pk=self.kwargs['quiz_pk'])
        except Quiz.DoesNotExist:
            return Response({
                "status_code": status.HTTP_404_NOT_FOUND,
                "error": "Quiz introuvable"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quiz=quiz)
            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "Question ajoutée avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": "Données invalides",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ReponseQuizViewSet(viewsets.ModelViewSet):
    serializer_class = ReponseQuizSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Récupérer directement les objets validés
                etudiant = serializer.validated_data['etudiant']
                question = serializer.validated_data['question']  # Objet déjà validé
                choix = serializer.validated_data['reponse']       # Objet déjà validé

                # Vérifier les doublons
                if ReponseQuiz.objects.filter(etudiant=etudiant, question=question).exists():
                    return Response({
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "error": "Réponse déjà existante"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Créer la réponse
                ReponseQuiz.objects.create(
                    etudiant=etudiant,
                    question=question,
                    reponse=choix
                )

                return Response({
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Réponse enregistrée",
                    "est_correct": choix.est_correct
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "error": "Erreur serveur",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": "Validation échouée",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ChoixQuizViewSet(viewsets.ModelViewSet):
    serializer_class = ChoixQuizSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        return ChoixQuiz.objects.filter(question_id=question_id)

    def create(self, request, *args, **kwargs):
        question = get_object_or_404(QuestionQuiz, pk=self.kwargs['question_pk'])
        serializer = self.get_serializer(data=request.data, many=True)
        
        if serializer.is_valid():
            serializer.save(question=question)
            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "Choix ajoutés avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": "Données invalides",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class QuestionQuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionQuizSerializer
    permission_classes = [AllowAny]
    queryset = QuestionQuiz.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            return Response({
                "status_code": status.HTTP_201_CREATED,
                "message": "Question et choix créés avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except serializers.ValidationError as e:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": str(e.detail)
            }, status=status.HTTP_400_BAD_REQUEST)
# formation/views.py
from formation.models.niveau import Niveaux
from quiz.models import QuestionQuiz, Quiz
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models.formation import Formation, Formateur, MoteCles
from .serializers import FormationFullSerializer, FormationSerializer, FormationDetailSerializer, MoteClesSerializer
from examen.models import Exam, QuestionExam
from test.models import ChoixTest, QuestionTest, Test
from django.db.models import Prefetch
class IsGerant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.utilisateur.type == 'gerant'

class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'by_formateur', 'full_details']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsGerant()]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return FormationDetailSerializer
        if self.action == 'full_details':
            return FormationFullSerializer
        return FormationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.utilisateur.type == 'gerant':
                return Formation.objects.all()
            if user.utilisateur.type == 'formateur':
                return Formation.objects.filter(formateur=user.utilisateur.formateur)
        return Formation.objects.all()

    def perform_create(self, serializer):
        formateur_id = self.request.data.get('formateur')
        try:
            formateur = Formateur.objects.get(ID_Utilisateur=formateur_id)
        except Formateur.DoesNotExist:
            raise ValidationError({"formateur": "Invalid Formateur ID"})
            
        serializer.save(formateur=formateur)

    @action(detail=False, methods=['get'], url_path='by-formateur/(?P<formateur_id>\d+)')
    def by_formateur(self, request, formateur_id=None):
        try:
            formations = Formation.objects.filter(formateur=formateur_id)
            serializer = self.get_serializer(formations, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"detail": "Invalid formateur ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='full-details')
    def full_details(self, request, pk=None):
        try:
            formation = Formation.objects.prefetch_related(
                Prefetch('niveaux', queryset=Niveaux.objects.prefetch_related(
                    Prefetch('cours'),
                    Prefetch('quizzes', queryset=Quiz.objects.prefetch_related(
                        Prefetch('questions', queryset=QuestionQuiz.objects.prefetch_related('choix'))
                    )),
                    Prefetch('exams', queryset=Exam.objects.prefetch_related(
                        Prefetch('questions', queryset=QuestionExam.objects.prefetch_related(
                            'choix',
                            'auto_correction',
                            'manual_correction'
                        ))
                    ))
                )),
                'mote_cles',
                'prerequis',
                Prefetch('tests', queryset=Test.objects.prefetch_related(
                 Prefetch('questions', queryset=QuestionTest.objects.prefetch_related(
                     Prefetch('auto_correction__choix')
                 ))
                 ))
            ).get(pk=pk)
            
            serializer = FormationFullSerializer(formation, context={'request': request})
            return Response(serializer.data)
        
        except Formation.DoesNotExist:
            return Response(
                {"detail": "Formation not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    @action(detail=False, methods=['get'], 
        url_path='by-formateur/(?P<formateur_id>\d+)/full-details')
    def by_formateur_full_details(self, request, formateur_id=None):
        try:
            formations = Formation.objects.filter(formateur=formateur_id).prefetch_related(
                # ... same prefetch logic as full_details ...
                Prefetch('niveaux', queryset=Niveaux.objects.prefetch_related(
                    Prefetch('cours'),
                    Prefetch('quizzes', queryset=Quiz.objects.prefetch_related(
                        Prefetch('questions', queryset=QuestionQuiz.objects.prefetch_related('choix'))
                    )),
                    Prefetch('exams', queryset=Exam.objects.prefetch_related(
                        Prefetch('questions', queryset=QuestionExam.objects.prefetch_related(
                            'choix',
                            'auto_correction',
                            'manual_correction'
                        ))
                    ))
                )),
                'mote_cles',
                'prerequis',
                Prefetch('tests', queryset=Test.objects.prefetch_related(
                    Prefetch('questions', queryset=QuestionTest.objects.prefetch_related(
                        Prefetch('auto_correction__choix')
                    ))
                ))
            )
            
            serializer = FormationFullSerializer(formations, many=True, context={'request': request})
            return Response(serializer.data)
        
        except ValueError:
            return Response(
                {"detail": "Invalid formateur ID"},
                status=status.HTTP_400_BAD_REQUEST
            )
class MoteClesViewSet(viewsets.ModelViewSet):
    queryset = MoteCles.objects.all()
    serializer_class = MoteClesSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsGerant()]
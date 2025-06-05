from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Question
from .serializers import QuestionSerializer
from formation.models.niveau import Niveaux

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-date_creation')

    def create(self, request, *args, **kwargs):
        # Authentication and validation
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'utilisateur'):
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.utilisateur.type != 'etudiant':
            return Response({"error": "Only students can create questions"}, status=status.HTTP_403_FORBIDDEN)

        # Prepare data
        data = request.data.copy()
        data['etudiant'] = user.utilisateur.ID_Utilisateur
        
        # Get formateur from niveau
        try:
            niveau = Niveaux.objects.get(id_niveau=data['niveau'])
            data['formateur'] = niveau.formation.formateur.ID_Utilisateur
        except (KeyError, Niveaux.DoesNotExist):
            return Response({"error": "Invalid niveau ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='respond')
    def respond_to_question(self, request, pk=None):
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'utilisateur'):
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.utilisateur.type != 'formateur':
            return Response({"error": "Only teachers can respond"}, status=status.HTTP_403_FORBIDDEN)

        question = self.get_object()
        if question.niveau.formation.formateur != user.utilisateur:
            return Response({"error": "Not your formation's question"}, status=status.HTTP_403_FORBIDDEN)

        question.reponse = request.data.get('reponse', '')
        question.save()
        
        return Response(self.get_serializer(question).data)

    def destroy(self, request, *args, **kwargs):
        question = self.get_object()
        user = request.user
        
        if not user.is_authenticated or not hasattr(user, 'utilisateur'):
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if question.niveau.formation.formateur != user.utilisateur:
            return Response({"error": "Can't delete others' questions"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)
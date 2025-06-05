from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all().order_by('-date')
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['patch'], url_path='gerant-response')
    def add_gerant_response(self, request, pk=None):
        feedback = self.get_object()
        if not request.user.utilisateur.type == 'gerant':
            return Response(
                {"error": "Only managers can respond"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        feedback.gerant_reponse = request.data.get('gerant_reponse')
        feedback.date_reponse = timezone.now()
        feedback.save()
        return Response(self.get_serializer(feedback).data)
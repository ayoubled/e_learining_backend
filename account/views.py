
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CompteSerializer, CustomTokenSerializer, RegistrationSerializer
from rest_framework import permissions
from rest_framework import viewsets
from .models import Compte, PointInterest, Diplome, Utilisateur
from .serializers import PointInterestSerializer, DiplomeSerializer,UserProfileSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer




class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.utilisateur.type == 'etudiant'

class IsFormateur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.utilisateur.type == 'formateur'

class PointInterestViewSet(viewsets.ModelViewSet):
    serializer_class = PointInterestSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return PointInterest.objects.filter(etudiant=self.request.user.utilisateur)

    def perform_create(self, serializer):
        serializer.save(etudiant=self.request.user.utilisateur)

class DiplomeViewSet(viewsets.ModelViewSet):
    serializer_class = DiplomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormateur]

    def get_queryset(self):
        return Diplome.objects.filter(formateur=self.request.user.utilisateur)

    def perform_create(self, serializer):
        serializer.save(formateur=self.request.user.utilisateur)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.utilisateur
    
class IsGerant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.utilisateur.type == 'gerant'
class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    permission_classes = [permissions.IsAuthenticated, IsGerant]
    lookup_field = 'email'  # Use email as the lookup field
    http_method_names = ['delete']  # Restrict to DELETE method only

class EtudiantListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Utilisateur.objects.filter(type='etudiant')

class FormateurListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Utilisateur.objects.filter(type='formateur')
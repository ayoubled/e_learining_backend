from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompteViewSet, EtudiantListView, FormateurListView, RegistrationView, CustomTokenView, PointInterestViewSet, DiplomeViewSet,UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'points', PointInterestViewSet, basename='pointinterest')
router.register(r'diplomes', DiplomeViewSet, basename='diplome')
router.register(r'comptes', CompteViewSet, basename='compte')
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomTokenView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('etudiants/', EtudiantListView.as_view(), name='etudiants-list'),
    path('formateurs/', FormateurListView.as_view(), name='formateurs-list'),
    path('', include(router.urls)),
]
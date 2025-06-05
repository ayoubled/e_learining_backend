from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormationViewSet, MoteClesViewSet  
from .niveau_views import NiveauxViewSet, InscritViewSet
from .cours_views import CoursViewSet

router = DefaultRouter()
router.register(r'formations', FormationViewSet, basename='formation')
router.register(r'mote-cles', MoteClesViewSet, basename='motecles')
router.register(r'niveaux', NiveauxViewSet, basename='niveaux')
urlpatterns = [
    path('', include(router.urls)),
    
    path('formations/<int:formation_pk>/niveaux/', 
         NiveauxViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='formation-niveaux-list'),
    path('formations/<int:formation_pk>/niveaux/<int:pk>/', 
         NiveauxViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='formation-niveaux-detail'),
    path('formations/<int:formation_pk>/niveaux/<int:niveau_pk>/inscrits/', 
         InscritViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='niveau-inscrits-list'),
    path('formations/<int:formation_pk>/niveaux/<int:niveau_pk>/inscrits/<int:pk>/', 
         InscritViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), 
         name='niveau-inscrits-detail'),
    path('formations/<int:formation_pk>/niveaux/<int:niveau_pk>/cours/',
         CoursViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='niveau-cours-list'),
    path('formations/<int:formation_pk>/niveaux/<int:niveau_pk>/cours/<int:pk>/',
         CoursViewSet.as_view({'get': 'retrieve', 'put': 'update', 
                              'patch': 'partial_update', 'delete': 'destroy'}),
         name='niveau-cours-detail'),
]
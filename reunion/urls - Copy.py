from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReunionViewSet, ConcerneReunionViewSet, ParticiperReunionViewSet

router = DefaultRouter()
router.register(r'reunions', ReunionViewSet, basename='reunion')
router.register(r'concerner', ConcerneReunionViewSet, basename='concerner')
router.register(r'participer', ParticiperReunionViewSet, basename='participer')

urlpatterns = [
    path('', include(router.urls)),
]
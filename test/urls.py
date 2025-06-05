# test/urls.py (updated)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestViewSet, 
    QuestionTestViewSet, 
    ChoixTestViewSet,
)
from .views_reponse import(
    ReponseTestManuelViewSet,
    ReponseTestAutoViewSet,
    EvaluationResultTestViewSet
)

router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls)),
    # Questions and choices
     path('tests/questions', 
         QuestionTestViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='test-questions'),
    path('questions/<int:question_id>/choices/', 
         ChoixTestViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='question-choices'),
    
    # Modified response endpoints with etudiant_id
    path('etudiants/<int:etudiant_id>/responses/manuel/', 
         ReponseTestManuelViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='manuel-responses'),
    path('etudiants/<int:etudiant_id>/responses/auto/', 
         ReponseTestAutoViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='auto-responses'),
    path('evaluations/', 
         EvaluationResultTestViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='evaluations'),
]
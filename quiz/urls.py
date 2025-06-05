from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'niveaux/quizzes', views.QuizViewSet, basename='quiz')
router.register(r'quizzes/(?P<quiz_pk>\d+)/questions', views.QuestionQuizViewSet, basename='question')
router.register(r'reponses', views.ReponseQuizViewSet, basename='reponse')
router.register(r'questions/(?P<question_pk>\d+)/choix', views.ChoixQuizViewSet, basename='choix')
router.register(r'questions', views.QuestionQuizViewSet, basename='questions')
urlpatterns = [
    path('', include(router.urls)),
]
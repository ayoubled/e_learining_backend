# examen/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Exam Endpoints
    path('exams/', views.ExamListCreate.as_view(), name='exam-list'),
    path('exams/<int:pk>/', views.ExamRetrieveUpdateDestroy.as_view(), name='exam-detail'),
    
    # Question Endpoints (Nested under Exams)
    
    path('questions/<int:pk>/', views.QuestionExamDetail.as_view(), name='question-detail'),
    path('questions/', views.QuestionExamListCreate.as_view(), name='question-list'),
    # Correction Endpoints (Nested under Questions)
    path('questions/<int:question_id>/auto-correction/', 
         views.AutoCorrectionExamCreate.as_view(),  
         name='auto-correction-create'),
    path('questions/<int:question_id>/manual-correction/', 
         views.ManuelCorrectionExamCreate.as_view(),  
         name='manual-correction-create'),
    
    # Choice Endpoints (Nested under Questions)
    path('questions/<int:question_id>/choices/', 
         views.ChoixExamListCreate.as_view(), 
         name='choice-list'),
    
    # Response Endpoints
    path('responses/auto/', 
         views.StudentResponseAutoCreate.as_view(), 
         name='auto-response-create'),
    path('responses/manual/', 
         views.StudentResponseManuelCreate.as_view(), 
         name='manual-response-create'),
   
    # Evaluation Endpoints
    path('evaluations/', 
         views.EvaluationResultCreate.as_view(), 
         name='evaluation-create'),
]
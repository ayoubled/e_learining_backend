# gere_formation/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.urls')),
    path('api/formation/', include('formation.urls')),
    path('api/test/', include('test.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/examen/', include('examen.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/questions/', include('question.urls')),
    path('api/reunion/', include('reunion.urls')),
]
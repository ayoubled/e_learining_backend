from django.db import models
from account.models import Utilisateur,Etudiant
from formation.models.niveau import Niveaux
class Quiz(models.Model):
    ID_Quiz = models.AutoField(primary_key=True)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE, related_name='quizzes')
    date_creation = models.DateTimeField(auto_now_add=True)

class QuestionQuiz(models.Model):
    ID_QuestionQuiz = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    contenu = models.TextField()
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

class ChoixQuiz(models.Model):
    ID_Choix_Quiz = models.AutoField(primary_key=True)
    question = models.ForeignKey(QuestionQuiz, on_delete=models.CASCADE, related_name='choix')
    contenu = models.CharField(max_length=255)
    est_correct = models.BooleanField(default=False)

class ReponseQuiz(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionQuiz, on_delete=models.CASCADE)
    reponse = models.ForeignKey(ChoixQuiz, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'question')
from django.db import models
from .models import QuestionTest, ChoixTest
from account.models import Etudiant, Formateur

class ReponseTestManuel(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTest, on_delete=models.CASCADE, 
                                limit_choices_to={'type': 'manuel'})
    reponse = models.TextField()

    class Meta:
        unique_together = [['etudiant', 'question']]

class ReponseTestAuto(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTest, on_delete=models.CASCADE,
                                limit_choices_to={'type': 'auto'})
    reponse = models.ForeignKey(ChoixTest, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['etudiant', 'question']]

class EvaluationResultTest(models.Model):
    reponse = models.OneToOneField(ReponseTestManuel, on_delete=models.CASCADE, 
                                  primary_key=True)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    note = models.PositiveIntegerField()
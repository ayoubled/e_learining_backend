
from django.db import models
from account.models import Utilisateur
from formation.models.niveau import Niveaux

class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    description = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions_etudiant',
        limit_choices_to={'type': 'etudiant'}
    )
    formateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions_formateur',
        limit_choices_to={'type': 'formateur'}
    )
    niveau = models.ForeignKey(
        Niveaux,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    
    def __str__(self):
        return f"Question {self.id_question} - {self.description[:50]}"
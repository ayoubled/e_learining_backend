from django.db import models
from account.models import Etudiant, Formateur

class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    note_sur_5 = models.PositiveIntegerField()
    etudiant = models.ForeignKey(
        Etudiant, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    formateur = models.ForeignKey(
        Formateur, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    gerant_reponse = models.TextField(blank=True, null=True)
    date_reponse = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Feedback #{self.id_feedback}"

from django.db import models
from account.models import Utilisateur
from formation.models.niveau import Niveaux

class Reunion(models.Model):
    id_reunion = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    date = models.DateTimeField()
    formateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='reunions_organisees',
        limit_choices_to={'type': 'formateur'}
    )
    niveaux = models.ManyToManyField(
        Niveaux,
        through='ConcerneReunion',
        related_name='reunions_concernees'
    )
    participants = models.ManyToManyField(
        Utilisateur,
        through='ParticiperReunion',
        related_name='reunions_participantes',
        limit_choices_to={'type': 'etudiant'}
    )

    def __str__(self):
        return f"{self.titre} - {self.date}"

class ConcerneReunion(models.Model):
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reunion', 'niveau')

class ParticiperReunion(models.Model):
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'etudiant'}
    )

    class Meta:
        unique_together = ('reunion', 'etudiant')
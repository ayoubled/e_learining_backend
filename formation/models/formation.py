from django.db import models

from account.models import Formateur ,Etudiant

class Formation(models.Model):
    id_formation = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=100)
    formateur = models.ForeignKey(
        Formateur,
        on_delete=models.CASCADE,
        related_name='formations_crees'
    )    
    def __str__(self):
        return self.titre
class MoteCles(models.Model):
    TYPE_CHOICES = [
        ('CONCEPT', 'Concept'),
        ('TECHNO', 'Technologie'),
        ('METHODE', 'Méthodologie'),
    ]
    
    id_mote_cles = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    formations = models.ManyToManyField(Formation, through='presiser' ,related_name='mote_cles')

    def __str__(self):
        return f"{self.get_type_display()}: {self.description}"

class presiser(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    mot_cle = models.ForeignKey(MoteCles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('formation', 'mot_cle')
class Requirement(models.Model):
    id_requirements = models.AutoField(primary_key=True)
    description = models.TextField()
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='prerequis'
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name_plural = "Requirements"

    def __str__(self):
        return f"{self.formation.titre} - Prerequis {self.ordre}"
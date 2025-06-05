
from django.db import models
from .niveau import Niveaux 


class Cours(models.Model):
    ID_Cours = models.AutoField(primary_key=True)
    Titre = models.CharField(max_length=200)
    Description = models.TextField()
    Duree = models.PositiveIntegerField(help_text="Duration in minutes")
    Type = models.CharField(max_length=20, choices=[
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('audio', 'Audio')
    ])
    url = models.URLField()
    niveau = models.ForeignKey(
        Niveaux,
        on_delete=models.CASCADE,
        related_name='cours'
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name_plural = "Cours"

    def __str__(self):
        return f"{self.Titre} - {self.Type}"
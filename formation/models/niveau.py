from django.db import models
from account.models import Etudiant
from formation.models.formation import Formation

class Niveaux(models.Model):
    id_niveau = models.AutoField(primary_key=True)
    description = models.TextField()
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='niveaux'
    )
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name_plural = "Niveaux"

    def __str__(self):
        return f"{self.formation.titre} - Niveau {self.ordre}"

class Inscrit(models.Model):
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    paye = models.BooleanField(default=False)

    class Meta:
        unique_together = ('niveau', 'etudiant')
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.etudiant} inscrit à {self.niveau}"
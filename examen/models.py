# examen/models.py
from django.db import models
from formation.models.niveau import Niveaux
from account.models import Formateur, Etudiant

class Exam(models.Model):
    id_exam = models.AutoField(primary_key=True)
    evaluation_state = models.BooleanField(
        default=False,
        verbose_name="Evaluation State",
        help_text="True = Evaluation open, False = Evaluation closed"
    )
    niveau = models.ForeignKey(
        Niveaux,
        on_delete=models.CASCADE,
        related_name='exams'
    )

    def __str__(self):
        status = "Open" if self.evaluation_state else "Closed"
        return f"Exam {self.id_exam} ({status})"


class QuestionExam(models.Model):
    QUESTION_TYPES = [
        ('auto', 'Auto-corrected'),
        ('manuel', 'Manual correction')
    ]
    
    id_question_exam = models.AutoField(primary_key=True)
    contenu = models.TextField()
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    def save(self, *args, **kwargs):
        """Automatically create/manage correction models on save"""
        creating = self._state.adding
        
        
        if not creating:
            old_instance = QuestionExam.objects.get(pk=self.pk)
            old_type = old_instance.type
        else:
            old_type = None

        super().save(*args, **kwargs)

        
        if self.type == 'auto':
            
            ManuelCorrectionExam.objects.filter(question=self).delete()
            
            if not hasattr(self, 'auto_correction'):
                AutoCorrectionExam.objects.create(question=self, note=1)
        elif self.type == 'manuel':
            
            AutoCorrectionExam.objects.filter(question=self).delete()
            
            if not hasattr(self, 'manual_correction'):
                ManuelCorrectionExam.objects.create(question=self)

class ManuelCorrectionExam(models.Model):
    question = models.OneToOneField(
        QuestionExam,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'type': 'manuel'},
        related_name='manual_correction'
    )

class AutoCorrectionExam(models.Model):
    question = models.OneToOneField(
        QuestionExam,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'type': 'auto'},
        related_name='auto_correction'
    )
    note = models.PositiveIntegerField()

class ChoixExam(models.Model):
    id_choix_exam = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    est_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        QuestionExam,
        on_delete=models.CASCADE,
        related_name='choix',
        limit_choices_to={'auto_correction__isnull': False}
    )

    class Meta:
        verbose_name_plural = "Choix Exams"

    def __str__(self):
        return f"Choix {self.id_choix_exam} ({'✓' if self.est_correct else '✗'})"

class ReponseExamAuto(models.Model):
    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='reponses_auto'
    )
    question = models.ForeignKey(
        QuestionExam,
        on_delete=models.CASCADE,
        limit_choices_to={'auto_correction__isnull': False}
    )
    choix = models.ForeignKey(
        ChoixExam,
        on_delete=models.CASCADE
    )
    date_passer_exam = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'question')
        verbose_name_plural = "Reponses Exam Auto"

    def __str__(self):
        return f"AutoResponse by {self.etudiant} to Q{self.question_id}"

class ReponseExamManuel(models.Model):
    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='reponses_manuel'
    )
    question = models.ForeignKey(
        QuestionExam,
        on_delete=models.CASCADE,
        limit_choices_to={'auto_correction__isnull': True}
    )
    reponse = models.TextField()
    date_passer_exam = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'question')
        verbose_name_plural = "Reponses Exam Manuel"

    def __str__(self):
        return f"ManualResponse by {self.etudiant} to Q{self.question_id}"

class EvaluationResultExam(models.Model):
    reponse = models.ForeignKey(
        ReponseExamManuel,
        on_delete=models.CASCADE,
        related_name='evaluations'
    )
    formateur = models.ForeignKey(
        Formateur,
        on_delete=models.CASCADE
    )
    note = models.FloatField()
    date_evaluation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reponse', 'formateur')
        verbose_name_plural = "Evaluation Results Exam"

    def __str__(self):
        return f"Evaluation by {self.formateur} - Note: {self.note}"
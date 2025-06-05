from django.db import models
from formation.models.formation import Formation

class Test(models.Model):
    ID_Test = models.AutoField(primary_key=True)
    Description = models.TextField()
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='tests'
    )

    def __str__(self):
        return f"Test {self.ID_Test} - {self.formation.Titre}"

class QuestionTest(models.Model):
    QUESTION_TYPES = [
        ('auto', 'Auto-corrected'),
        ('manuel', 'Manual correction')
    ]
    
    ID_QuestionTest = models.AutoField(primary_key=True)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    def save(self, *args, **kwargs):
        """Automatically create correction models when saving questions"""
        super().save(*args, **kwargs)
    
        if self.type == 'auto' and not hasattr(self, 'auto_correction'):
            AutoCorrectionTest.objects.create(question=self, note_question=1)
        elif self.type == 'manuel' and not hasattr(self, 'manual_correction'):
            ManuelCorrectionTest.objects.create(question=self)

class ManuelCorrectionTest(models.Model):
    question = models.OneToOneField(
        QuestionTest,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'type': 'manuel'},
        related_name='manual_correction'
    )

class AutoCorrectionTest(models.Model):
    question = models.OneToOneField(
        QuestionTest,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'type': 'auto'},
        related_name='auto_correction'
    )
    note_question = models.PositiveIntegerField()

class ChoixTest(models.Model):
    ID_ChoixTest = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    Est_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        AutoCorrectionTest,
        on_delete=models.CASCADE,
        related_name='choix'
    )
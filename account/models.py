from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CompteManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Compte(AbstractBaseUser, PermissionsMixin):  # Add PermissionsMixin
    email = models.EmailField(primary_key=True)
    mot_de_passe = models.CharField(max_length=128)
    etat = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin
    is_superuser = models.BooleanField(default=False)  # Required for superuser
    utilisateur = models.OneToOneField(
        'Utilisateur',
        on_delete=models.CASCADE,
        null=True,
        related_name='compte_rel'
    )
    
    USERNAME_FIELD = 'email'
    objects = CompteManager()

class Utilisateur(models.Model):
    ID_Utilisateur = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Date_naissance = models.DateField()
    Telephone = models.CharField(max_length=15)
    Sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    type = models.CharField(max_length=20, choices=[
        ('etudiant', 'Etudiant'),
        ('gerant', 'Gérant'),
        ('formateur', 'Formateur')
    ])

class Etudiant(models.Model):
    ID_Utilisateur = models.OneToOneField(
        Utilisateur, 
        primary_key=True, 
        on_delete=models.CASCADE,
        related_name='etudiant'
    )
    speciality = models.CharField(max_length=100)

class Gerant(models.Model):
    ID_Utilisateur = models.OneToOneField(
        Utilisateur, 
        primary_key=True, 
        on_delete=models.CASCADE,
        related_name='gerant'
    )

class Formateur(models.Model):
    ID_Utilisateur = models.OneToOneField(
        Utilisateur, 
        primary_key=True, 
        on_delete=models.CASCADE,
        related_name='formateur'
    )
    Domaine_expertise = models.CharField(max_length=100)
    Experience_annees = models.IntegerField()
class PointInterest(models.Model):
    ID_point_interest = models.AutoField(primary_key=True)
    point_interest = models.CharField(max_length=255)
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='points_interet',
        limit_choices_to={'type': 'etudiant'}
    )

    def __str__(self):
        return f"{self.point_interest} - {self.etudiant}"

class Diplome(models.Model):
    ID_Diplome = models.AutoField(primary_key=True)
    url = models.URLField(max_length=500)
    formateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='diplomes',
        limit_choices_to={'type': 'formateur'}
    )

    def __str__(self):
        return f"Diplôme {self.ID_Diplome} - {self.formateur}"
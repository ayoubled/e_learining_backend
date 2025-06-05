# account/admin.py
from django.contrib import admin
from .models import Compte, Utilisateur, Etudiant, Gerant, Formateur

admin.site.register(Compte)
admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(Gerant)
admin.site.register(Formateur)
# Generated by Django 5.2 on 2025-05-07 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_compte_groups_compte_is_staff_compte_is_superuser_and_more'),
        ('formation', '0003_cours'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionQuiz',
            fields=[
                ('ID_QuestionQuiz', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.TextField()),
                ('ordre', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['ordre'],
            },
        ),
        migrations.CreateModel(
            name='ChoixQuiz',
            fields=[
                ('ID_Choix_Quiz', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=255)),
                ('est_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choix', to='quiz.questionquiz')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('ID_Quiz', models.AutoField(primary_key=True, serialize=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='formation.niveaux')),
            ],
        ),
        migrations.AddField(
            model_name='questionquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.quiz'),
        ),
        migrations.CreateModel(
            name='ReponseQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_soumission', models.DateTimeField(auto_now_add=True)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.utilisateur')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questionquiz')),
                ('reponse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.choixquiz')),
            ],
            options={
                'unique_together': {('etudiant', 'question')},
            },
        ),
    ]

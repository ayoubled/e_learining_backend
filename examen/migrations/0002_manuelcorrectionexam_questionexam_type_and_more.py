# Generated by Django 5.2 on 2025-05-09 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManuelCorrectionExam',
            fields=[
                ('question', models.OneToOneField(limit_choices_to={'type': 'manuel'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='manual_correction', serialize=False, to='examen.questionexam')),
            ],
        ),
        migrations.AddField(
            model_name='questionexam',
            name='type',
            field=models.CharField(choices=[('auto', 'Auto-corrected'), ('manuel', 'Manual correction')], default='auto', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='autocorrectionexam',
            name='note',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='autocorrectionexam',
            name='question',
            field=models.OneToOneField(limit_choices_to={'type': 'auto'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='auto_correction', serialize=False, to='examen.questionexam'),
        ),
    ]

# Generated by Django 5.1 on 2024-11-15 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0010_openquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openquestion',
            name='pawn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openQuestions', to='pawns.pawn'),
        ),
    ]

# Generated by Django 5.1 on 2024-11-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0019_openanswer_freeze'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawn',
            name='partis_run',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.1 on 2024-09-08 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0013_remove_pawn_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawn',
            name='uuid',
            field=models.UUIDField(blank=True, default=None, null=True, unique=True),
        ),
    ]
# Generated by Django 5.1 on 2024-09-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0009_alter_pawn_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawn',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 5.1 on 2024-09-02 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0002_pawn_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='pawn',
            name='coze',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pawn',
            name='quiz',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.1 on 2024-11-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0018_alter_openanswer_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='openanswer',
            name='freeze',
            field=models.BooleanField(default=False),
        ),
    ]

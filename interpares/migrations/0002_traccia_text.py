# Generated by Django 5.1 on 2024-12-07 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interpares', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traccia',
            name='text',
            field=models.TextField(default=1, max_length=4096),
            preserve_default=False,
        ),
    ]

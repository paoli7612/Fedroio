# Generated by Django 5.1 on 2024-11-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0021_openquestion_correctanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgequestion',
            name='value',
            field=models.IntegerField(default=5),
        ),
    ]

# Generated by Django 5.1 on 2024-09-25 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(max_length=128)),
                ('pawn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='pawns.pawn')),
            ],
        ),
    ]

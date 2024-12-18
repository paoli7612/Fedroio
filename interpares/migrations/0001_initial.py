# Generated by Django 5.1 on 2024-11-22 09:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Traccia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=4096)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temi', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Griglia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_ortografia', models.IntegerField(blank=True, default=0, null=True)),
                ('forma_sintassi', models.IntegerField(blank=True, default=0, null=True)),
                ('forma_semantica', models.IntegerField(blank=True, default=0, null=True)),
                ('informazioni_sbagliate', models.IntegerField(blank=True, default=0, null=True)),
                ('informazioni_in_eccesso', models.IntegerField(blank=True, default=0, null=True)),
                ('informazioni_mancanti', models.IntegerField(blank=True, default=0, null=True)),
                ('discorso_diretto', models.IntegerField(blank=True, default=0, null=True)),
                ('figure_retoriche', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='griglie', to=settings.AUTH_USER_MODEL)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='griglie', to='interpares.tema')),
            ],
        ),
    ]

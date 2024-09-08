# Generated by Django 5.1 on 2024-09-08 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('pawns', '0010_pawn_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pawn',
            name='groups',
        ),
        migrations.AddField(
            model_name='pawn',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pawns', to='auth.group'),
        ),
    ]

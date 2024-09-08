# Generated by Django 5.1 on 2024-09-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('pawns', '0011_remove_pawn_groups_pawn_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pawn',
            name='group',
        ),
        migrations.AddField(
            model_name='pawn',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='pawns', to='auth.group'),
        ),
    ]

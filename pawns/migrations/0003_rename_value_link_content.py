# Generated by Django 5.1 on 2024-09-25 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pawns', '0002_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='value',
            new_name='content',
        ),
    ]

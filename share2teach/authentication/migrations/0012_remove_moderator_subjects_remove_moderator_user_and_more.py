# Generated by Django 5.1.1 on 2024-09-20 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_delete_userfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moderator',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='user',
        ),
        migrations.DeleteModel(
            name='Educator',
        ),
        migrations.DeleteModel(
            name='Moderator',
        ),
    ]

# Generated by Django 5.1 on 2024-09-20 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_uploadedfile_file_alter_uploadedfile_uploader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='uploader',
        ),
    ]

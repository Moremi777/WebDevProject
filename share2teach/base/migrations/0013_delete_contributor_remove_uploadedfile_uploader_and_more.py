# Generated by Django 5.1.1 on 2024-09-20 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_delete_subjects_delete_usersdemo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contributor',
        ),
        migrations.RemoveField(
            model_name='uploadedfile',
            name='uploader',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]

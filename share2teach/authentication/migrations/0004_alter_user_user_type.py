# Generated by Django 4.2.3 on 2024-08-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_subject_moderator_educator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('educator', 'Educator'), ('moderator', 'Moderator'), ('administrator', 'Administrator')], default='educator', max_length=20),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-21 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_newuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='registerid',
        ),
        migrations.AlterField(
            model_name='newuser',
            name='email',
            field=models.EmailField(max_length=25, unique=True),
        ),
    ]

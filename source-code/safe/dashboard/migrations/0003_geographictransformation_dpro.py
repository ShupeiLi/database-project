# Generated by Django 3.2.9 on 2022-01-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_geographictransformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='geographictransformation',
            name='dpro',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

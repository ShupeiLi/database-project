# Generated by Django 3.2.9 on 2021-12-21 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribution',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
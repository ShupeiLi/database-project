# Generated by Django 3.2.7 on 2021-12-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PathVisualization', '0004_auto_20211225_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geographicinformation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pandemicinformation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

# Generated by Django 3.2.7 on 2022-01-05 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PathVisualization', '0006_alter_pandemicinformation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pandemicinformation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]

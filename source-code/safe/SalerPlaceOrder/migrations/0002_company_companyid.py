# Generated by Django 2.2.5 on 2021-12-07 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalerPlaceOrder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='companyid',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
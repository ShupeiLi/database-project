# Generated by Django 2.2.5 on 2021-12-21 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SalerPlaceOrder', '0003_auto_20211220_0157'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.RenameField(
            model_name='salerinfo',
            old_name='companyid',
            new_name='company',
        ),
    ]

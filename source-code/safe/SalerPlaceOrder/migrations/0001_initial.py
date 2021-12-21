# Generated by Django 3.2.9 on 2021-12-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyid', models.CharField(max_length=200)),
                ('companyname', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SalerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salerid', models.CharField(max_length=200)),
                ('orderid', models.CharField(max_length=200)),
                ('companyid', models.CharField(default=0, max_length=200)),
            ],
        ),
    ]

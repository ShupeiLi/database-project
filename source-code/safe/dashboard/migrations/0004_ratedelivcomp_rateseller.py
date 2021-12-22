# Generated by Django 3.2.7 on 2021-12-22 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_delete_deliveryinformationmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('price', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('look', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('delivery', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('service', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('sellername', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rateforseller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RateDelivComp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('package', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('perfection', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('service', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('timely_feedback', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('compname', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rateforcompany', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

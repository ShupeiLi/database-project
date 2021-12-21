# Generated by Django 3.2.7 on 2021-12-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderBuyer',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=64)),
                ('price', models.FloatField()),
                ('number', models.IntegerField()),
                ('order_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderDelivComp',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('order_date', models.DateField()),
                ('in_time', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OrderEbPlat',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=64)),
                ('price', models.FloatField()),
                ('order_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderSeller',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('number', models.IntegerField()),
                ('order_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RateDelivComp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('speed', models.IntegerField()),
                ('package', models.IntegerField()),
                ('perfection', models.IntegerField()),
                ('service', models.IntegerField()),
                ('timely_feedback', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RateSeller',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quality', models.IntegerField()),
                ('price', models.IntegerField()),
                ('look', models.IntegerField()),
                ('delivery', models.IntegerField()),
                ('service', models.IntegerField()),
            ],
        ),
    ]

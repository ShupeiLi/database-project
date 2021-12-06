# Generated by Django 3.2.9 on 2021-12-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderConfirm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dno', models.CharField(max_length=100)),
                ('Dvalue', models.FloatField(max_length=50)),
                ('Dtrans', models.CharField(max_length=50)),
                ('Tno', models.CharField(max_length=50)),
                ('Sno', models.CharField(max_length=50)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]

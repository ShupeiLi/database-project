# Generated by Django 3.2.9 on 2022-01-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('utype', models.CharField(max_length=128)),
                ('companyname', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=25, unique=True)),
                ('registerdate', models.DateField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

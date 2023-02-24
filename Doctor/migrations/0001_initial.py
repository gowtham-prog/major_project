# Generated by Django 2.1.5 on 2023-02-22 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('patientname', models.CharField(max_length=100)),
                ('disease', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorLogin',
            fields=[
                ('doctorid', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('secquestion', models.CharField(max_length=200)),
                ('secanswer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorRegistration',
            fields=[
                ('doctorid', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('doctorname', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=1000)),
                ('education', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('specility', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('image', models.FileField(upload_to='')),
                ('city', models.CharField(max_length=50)),
            ],
        ),
    ]

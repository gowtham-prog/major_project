# Generated by Django 2.1.5 on 2023-02-23 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0003_auto_20230223_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]

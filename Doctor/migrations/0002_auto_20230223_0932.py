# Generated by Django 2.1.5 on 2023-02-23 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorregistration',
            name='image',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
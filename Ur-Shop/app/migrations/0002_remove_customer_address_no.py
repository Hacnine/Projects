# Generated by Django 4.0.3 on 2022-03-15 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='Address_no',
        ),
    ]

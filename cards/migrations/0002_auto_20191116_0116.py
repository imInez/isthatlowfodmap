# Generated by Django 2.2.7 on 2019-11-16 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal_name',
            field=models.CharField(max_length=100),
        ),
    ]

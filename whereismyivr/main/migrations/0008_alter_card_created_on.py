# Generated by Django 4.1.2 on 2022-11-05 22:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_card_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
    ]

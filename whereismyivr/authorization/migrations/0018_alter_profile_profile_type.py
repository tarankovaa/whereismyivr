# Generated by Django 4.1.2 on 2022-11-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0017_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_type',
            field=models.CharField(choices=[('PE', 'Исполнитель'), ('CU', 'Заказчик'), ('CO', 'Консультант')], default='PE', max_length=2, verbose_name='Тип профиля'),
        ),
    ]

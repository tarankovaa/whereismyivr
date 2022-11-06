# Generated by Django 4.1.2 on 2022-11-02 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Название')),
                ('type_of_app', models.CharField(choices=[('RE', 'Исследование'), ('PR', 'Проект')], max_length=2, verbose_name='Тип приложения')),
                ('looking_for', models.CharField(choices=[('CU', 'Заказчик'), ('CO', 'Консультант'), ('PE', 'Исполнитель'), ('PA', 'Напарник')], max_length=2, verbose_name='Поиск')),
                ('image', models.TextField(verbose_name='Образ продукта')),
            ],
        ),
    ]

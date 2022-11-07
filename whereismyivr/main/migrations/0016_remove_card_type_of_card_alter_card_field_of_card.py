# Generated by Django 4.1.2 on 2022-11-07 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_card_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='type_of_card',
        ),
        migrations.AlterField(
            model_name='card',
            name='field_of_card',
            field=models.CharField(choices=[('it_project', 'IT — проект'), ('business_project', 'Бизнес — проект'), ('design', 'Дизайн — проект'), ('publishing', 'Издательское дело — проект'), ('engineering', 'Инженерия — проект'), ('media', 'Медиа — проект'), ('education_project', 'Образование — проект'), ('events', 'Организация событий — проект'), ('it_research', 'IT — исследование'), ('business_research', 'Бизнес — исследование'), ('oriental_studies', 'Востоковедение — исследование'), ('natural_sciences', 'Естественные науки — исследование'), ('art', 'Искусствоведение — исследование'), ('history', 'История — исследование'), ('culturology', 'Культурология — исследование'), ('marketing', 'Маркетинг — исследование'), ('maths', 'Математика — исследование'), ('management', 'Менеджмент — исследование'), ('linguistics', 'Лингвистика — исследование'), ('education_research', 'Образование — исследование'), ('politics', 'Политология — исследование'), ('right', 'Право — исследование'), ('psychology', 'Психология — исследование'), ('sociology', 'Социология — исследование'), ('philology', 'Филология — исследование'), ('philosophy', 'Философия — исследование'), ('economy', 'Экономика — исследование')], max_length=20, verbose_name='Область'),
        ),
    ]

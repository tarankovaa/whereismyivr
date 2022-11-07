# Generated by Django 4.1.2 on 2022-11-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_card_field_alter_card_type_of_app'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='field',
            field=models.CharField(choices=[('it', 'IT'), ('business', 'Бизнес'), ('design', 'Дизайн'), ('publishing', 'Издательское дело'), ('engineering', 'Инженерия'), ('media', 'Медиа'), ('education', 'Образование'), ('events', 'Организация событий'), ('oriental_studies', 'Востоковедение'), ('natural_sciences', 'Естественные науки'), ('art', 'Искусствоведение'), ('history', 'История'), ('culturology', 'Культурология'), ('marketing', 'Маркетинг'), ('maths', 'Математика'), ('management', 'Менеджмент'), ('linguistics', 'Лингвистика'), ('politics', 'Политология'), ('right', 'Право'), ('psychology', ''), ('sociology', 'Социология'), ('philology', 'Филология'), ('philosophy', 'Философия'), ('economy', 'Экономика')], max_length=20, verbose_name='Область'),
        ),
    ]
# Generated by Django 4.1.2 on 2022-11-05 09:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authorization', '0003_alter_userprofile_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='User',
        ),
    ]
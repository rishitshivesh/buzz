# Generated by Django 3.1.1 on 2020-10-09 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='time',
            new_name='atime',
        ),
    ]

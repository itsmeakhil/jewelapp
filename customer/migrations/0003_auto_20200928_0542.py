# Generated by Django 3.1 on 2020-09-28 05:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0002_auto_20200928_0539'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerService',
            new_name='CustomerStatusData',
        ),
    ]

# Generated by Django 3.0.5 on 2020-12-04 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20201204_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerfieldreport',
            old_name='duraton_of_loan',
            new_name='duration_of_loan',
        ),
    ]
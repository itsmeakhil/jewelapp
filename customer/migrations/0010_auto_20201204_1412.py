# Generated by Django 3.0.5 on 2020-12-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20201204_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerfieldreport',
            name='marriage_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

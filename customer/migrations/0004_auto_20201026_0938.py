# Generated by Django 3.0.5 on 2020-10-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20201014_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

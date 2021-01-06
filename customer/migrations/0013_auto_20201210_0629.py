# Generated by Django 3.0.5 on 2020-12-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_auto_20201204_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerfieldreport',
            name='lat',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='customerfieldreport',
            name='lon',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customerfieldagent',
            name='status',
            field=models.IntegerField(choices=[(1, 'Open'), (2, 'Updated')], default=1),
        ),
    ]
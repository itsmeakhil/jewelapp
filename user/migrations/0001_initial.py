# Generated by Django 3.1 on 2020-09-28 05:39

from django.db import migrations, models
import django.db.models.deletion
import user.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('password', models.CharField(blank=True, max_length=150, null=True)),
                ('key', models.CharField(blank=True, default='', max_length=100)),
                ('push_notification_key', models.TextField(blank=True, default=' ', null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('user_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.usertype')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', user.manager.UserManager()),
            ],
        ),
    ]

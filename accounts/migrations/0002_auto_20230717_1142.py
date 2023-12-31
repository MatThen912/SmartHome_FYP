# Generated by Django 3.2 on 2023-07-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_staff',
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(blank=True, choices=[('Super Admin', 'Super Admin'), ('Admin', 'Admin'), ('User', 'User')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userpermissions',
            name='role',
            field=models.CharField(choices=[('Super Admin', 'Super Admin'), ('Admin', 'Admin'), ('User', 'User')], max_length=200),
        ),
    ]

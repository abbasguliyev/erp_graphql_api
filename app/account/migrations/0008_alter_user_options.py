# Generated by Django 3.2.12 on 2022-08-30 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_permissions': [], 'ordering': ('pk',), 'permissions': (('manage_users', 'Manage users'),)},
        ),
    ]

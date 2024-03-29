# Generated by Django 3.2.12 on 2022-08-31 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('cashbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycashbox',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.company'),
        ),
        migrations.AlterField(
            model_name='holdingcashbox',
            name='holding',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.holding'),
        ),
        migrations.AlterField(
            model_name='officecashbox',
            name='office',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.office'),
        ),
    ]

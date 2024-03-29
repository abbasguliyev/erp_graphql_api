# Generated by Django 4.0.7 on 2022-08-28 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeCashbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.office')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_officecashbox', 'Mövcud ofis cashboxlara baxa bilər'), ('add_officecashbox', 'Office cashbox əlavə edə bilər'), ('change_officecashbox', 'Office cashbox məlumatlarını yeniləyə bilər'), ('delete_officecashbox', 'Office cashbox silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='HoldingCashbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('holding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.holding')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_holdingcashbox', 'Mövcud holdinq cashboxlara baxa bilər'), ('add_holdingcashbox', 'Holdinq cashbox əlavə edə bilər'), ('change_holdingcashbox', 'Holdinq cashbox məlumatlarını yeniləyə bilər'), ('delete_holdingcashbox', 'Holdinq cashbox silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='CompanyCashbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashboxs', to='company.company')),
            ],
            options={
                'ordering': ('pk',),
                'permissions': (('view_companycashbox', 'Mövcud şirkət cashboxlara baxa bilər'), ('add_companycashbox', 'Şirkət cashbox əlavə edə bilər'), ('change_companycashbox', 'Şirkət cashbox məlumatlarını yeniləyə bilər'), ('delete_companycashbox', 'Şirkət cashbox silə bilər')),
                'default_permissions': [],
            },
        ),
        migrations.CreateModel(
            name='CashFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('initial_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('subsequent_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('holding_initial_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('holding_subsequent_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('company_initial_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('company_subsequent_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('office_initial_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('office_subsequent_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('operation_style', models.CharField(blank=True, choices=[('MƏDAXİL', 'MƏDAXİL'), ('MƏXARİC', 'MƏXARİC'), ('TRANSFER', 'TRANSFER')], default=None, max_length=100, null=True)),
                ('quantity', models.FloatField(default=0)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='company.company')),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to=settings.AUTH_USER_MODEL)),
                ('holding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='company.holding')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows', to='company.office')),
            ],
            options={
                'ordering': ('-pk',),
                'permissions': (('view_cashflow', 'Mövcud pul axınlarına baxa bilər'), ('add_cashflow', 'Pul axını əlavə edə bilər'), ('change_cashflow', 'Pul axını məlumatlarını yeniləyə bilər'), ('delete_cashflow', 'Pul axını məlumatlarını silə bilər')),
                'default_permissions': [],
            },
        ),
    ]

from salary.models import MaasGoruntuleme
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd
from holiday.models import EmployeeWorkingDay

@receiver(post_save, sender=User)
def create_employee_maas_goruntulenme(sender, instance, created, **kwargs):
    if created:
        user = instance
        indi = datetime.date.today()
        
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
       
        next_m = d + pd.offsets.MonthBegin(1)
        
        employee_maas_bu_ay = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_maas_bu_ay) == 0:
            if user.salary_style == "FİX":
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}").save()

        employee_maas_novbeti_ay = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(employee_maas_novbeti_ay) == 0:
            if user.salary_style == "FİX":
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}").save()

@receiver(post_save, sender=User)
def create_employee_working_day(sender, instance, created, **kwargs):
    if created:
        user = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        employee_working_day_this_month = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_working_day_this_month) == 0:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            employee_working_day.save()

        employee_working_day = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(employee_working_day) == 0:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_mont,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            employee_working_day.save()

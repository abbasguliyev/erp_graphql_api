import datetime
from company.models import Position
from .models import User
from celery import shared_task
import pandas as pd
from salary.models import CanvasserPrim, SalaryView, OfficeLeaderPrim

@shared_task(name='salary_view_create_task')
def salary_view_create_task():
    users = User.objects.all()
    now = datetime.date.today()
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        employee_salary = SalaryView.objects.select_related('employee').filter(
            employee=user, 
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(employee_salary) != 0:
            continue
        else:
            SalaryView.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", final_salary=user.salary).save()
            
    for user in users:
        employee_salary = SalaryView.objects.select_related('employee').filter(
            employee=user, 
            date__year = now.year,
            date__month = now.month
        )
        if len(employee_salary) != 0:
            continue
        else:
            SalaryView.objects.create(employee=user, date=f"{now.year}-{now.month}-{1}", final_salary=user.salary).save()

@shared_task(name='employee_fix_prim_auto_add')
def employee_fix_prim_auto_add():
    now = datetime.date.today()

    this_month = f"{now.year}-{now.month}-{1}"
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    previus_month = d - pd.offsets.MonthBegin(1)

    officeLeaderPosition = Position.objects.filter(name="OFFICE LEADER")[0]
    officeLeaders = User.objects.filter(position__name=officeLeaderPosition.name)

    for officeLeader in officeLeaders:
        officeLeader_status = officeLeader.employee_status

        officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeader.position)
        officeLeader_salary_view_this_month = SalaryView.objects.get(employee=officeLeader, date=this_month)

        officeLeader_salary_view_this_month.final_salary = float(officeLeader_salary_view_this_month.final_salary) + float(officeleader_prim.fix_prim)
        officeLeader_salary_view_this_month.save()

    canvasserPosition = Position.objects.filter(name="CANVASSER")[0]
    canvassers = User.objects.filter(position__name=canvasserPosition.name)

    for responsible_employee_3 in canvassers:
        responsible_employee_3_status = responsible_employee_3.employee_status

        responsible_employee_3_prim = CanvasserPrim.objects.get(prim_status=responsible_employee_3_status, position=responsible_employee_3.position)

        responsible_employee_3_salary_view_previus_month = SalaryView.objects.get(employee=responsible_employee_3, date=previus_month)
        responsible_employee_3_salary_view_this_month = SalaryView.objects.get(employee=responsible_employee_3, date=f"{now.year}-{now.month}-{1}")

        prim_for_sales_quantity = 0
        if (responsible_employee_3_salary_view_previus_month.sales_quantity == 0):
            prim_for_sales_quantity = responsible_employee_3_prim.sale_0
        elif (responsible_employee_3_salary_view_previus_month.sales_quantity >= 1) and (responsible_employee_3_salary_view_previus_month.sales_quantity <= 8):
            prim_for_sales_quantity = responsible_employee_3_prim.sale_1_8

        responsible_employee_3_salary_view_this_month.final_salary = float(responsible_employee_3_salary_view_this_month.final_salary) + float(prim_for_sales_quantity) + float(responsible_employee_3_prim.fix_prim)
        responsible_employee_3_salary_view_this_month.save()
        responsible_employee_3_salary_view_previus_month.save()
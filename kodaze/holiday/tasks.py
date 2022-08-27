from celery import shared_task
import pandas as pd

import datetime
from account.models import User
from company.models import Holding, Team, Office, Company, Department, Position
from .models import (
    HoldingWorkingDay,
    EmployeeWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    DepartmentWorkingDay,
    PositionWorkingDay
)

# Isci working_day ---------------------------------------------------
@shared_task(name='work_day_creater_task')
def work_day_creater_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = User.objects.all()

    for user in users:
        employee_working_day = EmployeeWorkingDay.objects.select_related("employee").filter(
            employee = user,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(employee_working_day) != 0:
            continue
        else:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            employee_working_day.save()

    for user in users:
        employee_working_day = EmployeeWorkingDay.objects.select_related("employee").filter(
            employee = user,
            date__year = now.year,
            date__month = now.month
        )
        if len(employee_working_day) != 0:
            continue
        else:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            employee_working_day.save()

# Holding working_day ---------------------------------------------------
@shared_task(name='work_day_creater_holding_task')
def work_day_creater_holding_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holdings = Holding.objects.all()

    for holding in holdings:
        holding_working_day = HoldingWorkingDay.objects.select_related("holding").filter(
            holding = holding,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(holding_working_day) != 0:
            continue
        else:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_working_day.save()
    
    for holding in holdings:
        holding_working_day = HoldingWorkingDay.objects.select_related("holding").filter(
            holding = holding,
            date__year = now.year,
            date__month = now.month
        )
        if len(holding_working_day) != 0:
            continue
        else:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            holding_working_day.save()

# Company working_day ---------------------------------------------------
@shared_task(name='work_day_creater_company_task')
def work_day_creater_company_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    companyler = Company.objects.all()

    for company in companyler:
        company_working_day = CompanyWorkingDay.objects.select_related("company").filter(
            company = company,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(company_working_day) != 0:
            continue
        else:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            company_working_day.save()
    for company in companyler:
        company_working_day = CompanyWorkingDay.objects.select_related("company").filter(
            company = company,
            date__year = now.year,
            date__month = now.month
        )
        if len(company_working_day) != 0:
            continue
        else:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            company_working_day.save()


# Office working_day ---------------------------------------------------
@shared_task(name='work_day_creater_office_task')
def work_day_creater_office_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    officeler = Office.objects.all()

    for office in officeler:
        office_working_day = OfficeWorkingDay.objects.select_related("office").filter(
            office = office,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(office_working_day) != 0:
            continue
        else:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            office_working_day.save()

    for office in officeler:
        office_working_day = OfficeWorkingDay.objects.select_related("office").filter(
            office = office,
            date__year = now.year,
            date__month = now.month
        )
        if len(office_working_day) != 0:
            continue
        else:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            office_working_day.save()

# Department working_day ---------------------------------------------------
@shared_task(name='work_day_creater_department_task')
def work_day_creater_department_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    departmentler = Department.objects.all()

    for department in departmentler:
        department_working_day = DepartmentWorkingDay.objects.select_related("department").filter(
            department = department,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(department_working_day) != 0:
            continue
        else:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            department_working_day.save()
    for department in departmentler:
        department_working_day = DepartmentWorkingDay.objects.select_related("department").filter(
            department = department,
            date__year = now.year,
            date__month = now.month
        )
        if len(department_working_day) != 0:
            continue
        else:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            department_working_day.save()

# Team working_day ---------------------------------------------------
@shared_task(name='work_day_creater_team_task')
def work_day_creater_team_task():
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    teamlar = Team.objects.all()

    position = Position.objects.all()

    for team in teamlar:
        team_working_day = TeamWorkingDay.objects.select_related("team").filter(
            team = team,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(team_working_day) != 0:
            continue
        else:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            team_working_day.save()
    
    for team in teamlar:
        team_working_day = TeamWorkingDay.objects.select_related("team").filter(
            team = team,
            date__year = now.year,
            date__month = now.month
        )
        if len(team_working_day) != 0:
            continue
        else:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            team_working_day.save()

# Position working_day ---------------------------------------------------
@shared_task(name='work_day_creater_position_task')
def work_day_creater_position_task():
    """
    İş və tətil günlərini create edən task
    """
    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    position = Position.objects.all()

    for position in position:
        position_working_day = PositionWorkingDay.objects.select_related("position").filter(
            position = position,
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(position_working_day) != 0:
            continue
        else:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            position_working_day.save()
    
    for position in position:
        position_working_day = PositionWorkingDay.objects.select_related("position").filter(
            position = position,
            date__year =  now.year,
            date__month = now.month
        )
        if len(position_working_day) != 0:
            continue
        else:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_this_month,
                date = f"{now.year}-{now.month}-{1}"
            )
            position_working_day.save()


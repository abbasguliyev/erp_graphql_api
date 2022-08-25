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
@shared_task(name='work_day_creater_task1')
def work_day_creater_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = User.objects.all()

    for user in users:
        employee_working_day = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        employee_working_day = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_working_day) != 0:
            continue
        else:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            employee_working_day.save()


@shared_task(name='work_day_creater_task15')
def work_day_creater_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = User.objects.all()

    for user in users:
        employee_working_day = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        employee_working_day = EmployeeWorkingDay.objects.filter(
            employee = user,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_working_day) != 0:
            continue
        else:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee = user,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            employee_working_day.save()

# Holding working_day ---------------------------------------------------
@shared_task(name='work_day_creater_holding_task1')
def work_day_creater_holding_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holdings = Holding.objects.all()

    for holding in holdings:
        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_working_day) != 0:
            continue
        else:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            holding_working_day.save()

@shared_task(name='work_day_creater_holding_task15')
def work_day_creater_holding_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    holdings = Holding.objects.all()

    for holding in holdings:
        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_working_day) != 0:
            continue
        else:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            holding_working_day.save()

# Company working_day ---------------------------------------------------
@shared_task(name='work_day_creater_company_task1')
def work_day_creater_company_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    companyler = Company.objects.all()

    for company in companyler:
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(company_working_day) != 0:
            continue
        else:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            company_working_day.save()

@shared_task(name='work_day_creater_company_task15')
def work_day_creater_company_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    companyler = Company.objects.all()

    for company in companyler:
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(company_working_day) != 0:
            continue
        else:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            company_working_day.save()


# Office working_day ---------------------------------------------------
@shared_task(name='work_day_creater_office_task1')
def work_day_creater_office_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    officeler = Office.objects.all()

    for office in officeler:
        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(office_working_day) != 0:
            continue
        else:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            office_working_day.save()

@shared_task(name='work_day_creater_office_task15')
def work_day_creater_office_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    officeler = Office.objects.all()

    for office in officeler:
        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(office_working_day) != 0:
            continue
        else:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            office_working_day.save()

# Department working_day ---------------------------------------------------
@shared_task(name='work_day_creater_department_task1')
def work_day_creater_department_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    departmentler = Department.objects.all()

    for department in departmentler:
        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(department_working_day) != 0:
            continue
        else:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            department_working_day.save()

@shared_task(name='work_day_creater_department_task15')
def work_day_creater_department_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    departmentler = Department.objects.all()

    for department in departmentler:
        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(department_working_day) != 0:
            continue
        else:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            department_working_day.save()


# Team working_day ---------------------------------------------------
@shared_task(name='work_day_creater_team_task1')
def work_day_creater_team_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    teamlar = Team.objects.all()

    position = Position.objects.all()

    for team in teamlar:
        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(team_working_day) != 0:
            continue
        else:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            team_working_day.save()

@shared_task(name='work_day_creater_team_task15')
def work_day_creater_team_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    teamlar = Team.objects.all()

    for team in teamlar:
        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(team_working_day) != 0:
            continue
        else:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            team_working_day.save()


# Position working_day ---------------------------------------------------
@shared_task(name='work_day_creater_position_task1')
def work_day_creater_position_task1():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    position = Position.objects.all()

    for position in position:
        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(position_working_day) != 0:
            continue
        else:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            position_working_day.save()



@shared_task(name='work_day_creater_position_task15')
def work_day_creater_position_task15():
    """
    İş və tətil günlərini create edən task
    """
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

    days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    position = Position.objects.all()

    for position in position:
        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year = next_m.year,
            tarix__month = next_m.month
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
        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(position_working_day) != 0:
            continue
        else:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            position_working_day.save()
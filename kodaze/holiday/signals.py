from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

import datetime
from company.models import Holding, Team, Office, Company, Department, Position
from .models import (
    HoldingWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    DepartmentWorkingDay,
    PositionWorkingDay
)

# Holding working_day ---------------------------------------------------
@receiver(post_save, sender=Holding)
def holding_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        holding = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(holding_working_day) == 0:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            holding_working_day.save()
        
        holding_working_day = HoldingWorkingDay.objects.filter(
            holding = holding,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(holding_working_day) == 0:
            holding_working_day = HoldingWorkingDay.objects.create(
                holding = holding,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            holding_working_day.save()

# Company working_day ---------------------------------------------------
@receiver(post_save, sender=Company)
def company_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        company = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(company_working_day) == 0:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            company_working_day.save()
        
        company_working_day = CompanyWorkingDay.objects.filter(
            company = company,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(company_working_day) == 0:
            company_working_day = CompanyWorkingDay.objects.create(
                company = company,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            company_working_day.save()

# Office working_day ---------------------------------------------------
@receiver(post_save, sender=Office)
def office_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        office = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(office_working_day) == 0:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            office_working_day.save()

    
        office_working_day = OfficeWorkingDay.objects.filter(
            office = office,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(office_working_day) == 0:
            office_working_day = OfficeWorkingDay.objects.create(
                office = office,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            office_working_day.save()

# Department working_day ---------------------------------------------------
@receiver(post_save, sender=Department)
def department_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        department = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(department_working_day) == 0:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            department_working_day.save()
        department_working_day = DepartmentWorkingDay.objects.filter(
            department = department,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(department_working_day) == 0:
            department_working_day = DepartmentWorkingDay.objects.create(
                department = department,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            department_working_day.save()

# Team working_day ---------------------------------------------------
@receiver(post_save, sender=Team)
def team_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        team = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(team_working_day) == 0:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            team_working_day.save()
    
        team_working_day = TeamWorkingDay.objects.filter(
            team = team,
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(team_working_day) == 0:
            team_working_day = TeamWorkingDay.objects.create(
                team = team,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            team_working_day.save()

# Position working_day ---------------------------------------------------
@receiver(post_save, sender=Position)
def position_working_day_create(sender, instance, created, **kwargs):
    """
    İş və tətil günlərini create edən task
    """
    if created:
        position = instance
        indi = datetime.date.today()

        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(f"{indi.year}-{indi.month}-{1}").days_in_month

        days_in_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month


        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(position_working_day) == 0:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_month,
                date = f"{next_m.year}-{next_m.month}-{1}"
            )
            position_working_day.save()
    
        position_working_day = PositionWorkingDay.objects.filter(
            position = position,
            tarix__year =  indi.year,
            tarix__month = indi.month
        )
        if len(position_working_day) == 0:
            position_working_day = PositionWorkingDay.objects.create(
                position = position,
                working_days_count=days_in_this_month,
                date = f"{indi.year}-{indi.month}-{1}"
            )
            position_working_day.save()
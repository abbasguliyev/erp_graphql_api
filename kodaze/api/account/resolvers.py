from account.models import (
    Customer,
    CustomerNote,
    EmployeeStatus,
    Region,
)
from django.contrib.auth import get_user_model

User = get_user_model()


def resolve_cutomer(id):
    return Customer.objects.select_related('region', 'executor').filter(id=id).first()


def resolve_customers():
    return Customer.objects.select_related('region', 'executor').all()


def resolve_cutomer_note(id):
    return CustomerNote.objects.select_related('customer').filter(id=id).first()


def resolve_cutomer_notes():
    return CustomerNote.objects.select_related('customer').all()


def resolve_employee_status(id):
    return EmployeeStatus.objects.filter(id=id).first()


def resolve_employee_statuses(id):
    return EmployeeStatus.objects.all()


def resolve_region(id):
    return Region.objects.filter(id=id).first()


def resolve_regions(id):
    return Region.objects.all()


def resolve_user(id):
    return User.objects.select_related(
        'company', 'office', 'department', 'position', 'team', 'employee_status', 'supervisor'
    ).filter(id=id).first()


def resolve_users(id):
    return User.objects.select_related(
        'company', 'office', 'department', 'position', 'team', 'employee_status', 'supervisor'
    ).all()

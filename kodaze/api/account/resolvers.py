from account.models import (
    Customer,
    CustomerNote,
    EmployeeStatus,
    Region,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

User = get_user_model()


def resolve_permission(id):
    return Permission.objects.filter(id=id).first()


def resolve_permissions():
    return Permission.objects.all()


def resolve_group(id):
    return Group.objects.filter(id=id).first()


def resolve_groups():
    return Group.objects.all()


def resolve_customer(id):
    return Customer.objects.select_related('region', 'executor').filter(id=id).first()


def resolve_customers():
    return Customer.objects.select_related('region', 'executor').all()


def resolve_customer_note(id):
    return CustomerNote.objects.select_related('customer').filter(id=id).first()


def resolve_customer_notes():
    return CustomerNote.objects.select_related('customer').all()


def resolve_employee_status(id):
    return EmployeeStatus.objects.filter(id=id).first()


def resolve_employee_statuses():
    return EmployeeStatus.objects.all()


def resolve_region(id):
    return Region.objects.filter(id=id).first()


def resolve_regions():
    return Region.objects.all()


def resolve_user(id):
    return User.objects.select_related(
        'company', 'office', 'department', 'position', 'team', 'employee_status', 'supervisor'
    ).filter(id=id).first()


def resolve_users():
    return User.objects.select_related(
        'company', 'office', 'department', 'position', 'team', 'employee_status', 'supervisor'
    ).all()

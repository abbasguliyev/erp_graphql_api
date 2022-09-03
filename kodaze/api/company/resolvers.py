from company.models import (
    Company,
    Holding,
    Office,
    Team,
    Department,
    PermissionForPosition,
    Position,
    AppLogo
)


def resolve_holding(id):
    return Holding.objects.filter(id=id).first()


def resolve_holdings():
    return Holding.objects.all()


def resolve_company(id):
    return Company.objects.select_related('holding').filter(id=id).first()


def resolve_companies():
    return Company.objects.select_related('holding').all()


def resolve_office(id):
    return Office.objects.select_related('company').filter(id=id).first()


def resolve_offices():
    return Office.objects.select_related('company').all()


def resolve_department(id):
    return Department.objects.select_related('office').filter(id=id).first()


def resolve_departments():
    return Department.objects.select_related('office').all()


def resolve_position(id):
    return Position.objects.filter(id=id).first()


def resolve_positions():
    return Position.objects.all()


def resolve_team(id):
    return Team.objects.filter(id=id).first()


def resolve_teams():
    return Team.objects.all()


def resolve_permission_for_position(id):
    return PermissionForPosition.objects.select_related('position', 'permission_group').filter(id=id).first()


def resolve_permission_for_positions():
    return PermissionForPosition.objects.select_related('position', 'permission_group').all()


def resolve_app_logo(id):
    return AppLogo.objects.filter(id=id).first()


def resolve_app_logos():
    return AppLogo.objects.all()

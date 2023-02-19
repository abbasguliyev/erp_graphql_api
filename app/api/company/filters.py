import django_filters

from company.models import (
    Company,
    Office,
    Team,
    Department,
    PermissionForPosition,
    Position,
)

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class OfficeFilter(django_filters.FilterSet):
    class Meta:
        model = Office
        fields = {
            'name': ['exact', 'icontains'],
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            'name': ['exact', 'icontains'],
            'ofis': ['exact'],
            'ofis__id': ['exact'],
            'ofis__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class VezifeFilter(django_filters.FilterSet):
    class Meta:
        model = Position
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'department__id': ['exact'],
            'department__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class PermissionForPositionFilter(django_filters.FilterSet):
    class Meta:
        model = PermissionForPosition
        fields = {
            'position__name': ['exact', 'icontains']
        }

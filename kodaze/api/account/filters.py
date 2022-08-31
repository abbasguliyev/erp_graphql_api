from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.auth.models import Permission, Group
import django_filters

from account.models import (
    Customer,
    CustomerNote,
    EmployeeStatus,
    Region,
)
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import Permission, Group

User = get_user_model()


class PermissionFilter(django_filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'content_type': ['exact'],
            'codename': ['exact', 'icontains']
        }


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'permissions': ['exact', 'icontains']
        }

class UserFilter(django_filters.FilterSet):
    date_of_birth = django_filters.DateFilter(
        field_name='date_of_birth', input_formats=["%d-%m-%Y"])
    start_date_of_work = django_filters.DateFilter(
        field_name='start_date_of_work', input_formats=["%d-%m-%Y"])
    start_date_of_work__gte = django_filters.DateFilter(
        field_name='start_date_of_work', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    start_date_of_work__lte = django_filters.DateFilter(
        field_name='start_date_of_work', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    dismissal_date = django_filters.DateFilter(
        field_name='dismissal_date', input_formats=["%d-%m-%Y"])
    dismissal_date__gte = django_filters.DateFilter(
        field_name='dismissal_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    dismissal_date__lte = django_filters.DateFilter(
        field_name='dismissal_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    fullname = django_filters.CharFilter(method="fullname_filter")
    supervisor_fullname = django_filters.CharFilter(
        method="supervisor_fullname_filter")

    class Meta:
        model = User
        fields = {
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'phone_number_1': ['exact', 'icontains'],
            'phone_number_2': ['exact', 'icontains'],
            'position__name': ['exact', 'icontains'],
            'position': ['exact'],
            'is_superuser': ['exact'],

            'company__name': ['exact', 'icontains'],
            'office__name': ['exact', 'icontains'],
            'department__name': ['exact', 'icontains'],
            'team__name': ['exact', 'icontains'],
            'supervisor': ['exact'],
            'is_active': ['exact'],
            'employee_status__status_name': ['exact', 'icontains'],
        }

    def fullname_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = User.objects.filter(
                Q(first_name__icontains=term) | Q(last_name__icontains=term))
        return qs

    def supervisor_fullname_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = User.objects.filter(Q(supervisor__first_name__icontains=term) | Q(
                supervisor__last_name__icontains=term))
        return qs


class EmployeeStatusFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeStatus
        fields = {
            'status_name': ['exact', 'icontains'],
        }


class RegionFilter(django_filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            'region_name': ['exact', 'icontains'],
        }


class CustomerFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(method="fullname_filter")
    phone_number = django_filters.CharFilter(method="phone_number_filter")
    executor_fullname = django_filters.CharFilter(
        method="executor_fullname_filter")

    class Meta:
        model = Customer
        fields = {
            'phone_number_1': ['exact', 'icontains'],
            'phone_number_2': ['exact', 'icontains'],
            'phone_number_3': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'order_count': ['exact', 'gte', 'lte'],
            'is_active': ['exact'],
            'address': ['exact', 'icontains'],
            'executor': ['exact'],
            'executor__company': ['exact'],
            'executor__company__name': ['exact', 'icontains'],
            'executor__office': ['exact'],
            'executor__office__name': ['exact', 'icontains'],
            'region__region_name': ['exact', 'icontains'],
        }

    def phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = Customer.objects.filter(
                Q(phone_number_1__icontains=term) | Q(phone_number_2__icontains=term) | Q(phone_number_3__icontains=term))
        return qs
    
    def fullname_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = Customer.objects.filter(
                Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(father_name__icontains=term))
        return qs

    def executor_fullname_filter(self, queryset, name, value):
        qs=None
        for term in value.split():
            qs=Customer.objects.filter(Q(executor__first_name__icontains=term) | Q(
                executor__last_name__icontains=term))
        return qs


class CustomerNoteFilter(django_filters.FilterSet):
    date=django_filters.DateFilter(
        field_name = 'date', input_formats = ["%d-%m-%Y"])
    date__gte=django_filters.DateFilter(
        field_name = 'date', lookup_expr = 'gte', input_formats = ["%d-%m-%Y"])
    date__lte=django_filters.DateFilter(
        field_name = 'date', lookup_expr = 'lte', input_formats = ["%d-%m-%Y"])
    customer_fullname=django_filters.CharFilter(
        method = "customer_fullname_filter")

    class Meta:
        model=CustomerNote
        fields={
            'customer': ['exact'],
            'customer__phone_number_1': ['exact', 'icontains'],
            'customer__phone_number_2': ['exact', 'icontains'],
            'customer__phone_number_3': ['exact', 'icontains'],
            'customer__email': ['exact', 'icontains'],
            'customer__region__region_name': ['exact', 'icontains'],
            'customer__region': ['exact'],
            'note': ['exact', 'icontains'],
        }

    def customer_fullname_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = CustomerNote.objects.filter(Q(customer__first_name__icontains=term) | Q(
                customer__last_name__icontains=term) | Q(
                customer__father_name__icontains=term))
        return qs

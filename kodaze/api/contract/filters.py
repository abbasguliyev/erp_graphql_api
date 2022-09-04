# import django_filters

# from contract.models import (
#     ContractGift,
#     Contract,
#     Installment,
#     DemoSales
# )
# from django.db.models import Q


# class InstallmentFilter(django_filters.FilterSet):
#     contract__contract_date = django_filters.DateFilter(
#         field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
#     contract__contract_date__gte = django_filters.DateFilter(
#         field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     contract__contract_date__lte = django_filters.DateFilter(
#         field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     date = django_filters.DateFilter(
#         field_name='date', input_formats=["%d-%m-%Y"])
#     date__gte = django_filters.DateFilter(
#         field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     date__lte = django_filters.DateFilter(
#         field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     contract_customer_fullname = django_filters.CharFilter(
#         method="contract_customer_fullname_filter")

#     contract_customer_phone_number = django_filters.CharFilter(
#         method="contract_customer_phone_number_filter")

#     contract__creditors__creditor_fullname = django_filters.CharFilter(
#         method="contract__creditors__creditor_fullname_filter")
    
#     class Meta:
#         model = Installment
#         fields = {
#             'contract': ['exact'],
#             'contract__office__name': ['exact', 'icontains'],
#             'contract__company__name': ['exact', 'icontains'],

#             # 'contract__responsible_employee_1__asa': ['exact', 'icontains'],
#             'contract__responsible_employee_1__team__name': ['exact', 'icontains'],
#             'contract__responsible_employee_1__employee_status__status_name': ['exact', 'icontains'],

#             'contract__payment_style': ['exact'],
#             'contract__creditors__creditor': ['exact'],
#             'contract__contract_status': ['exact'],
#             'contract__total_amount': ['exact', 'gte', 'lte'],
#             'contract__product_quantity': ['exact', 'gte', 'lte'],

#             'contract__customer__address': ['exact', 'icontains'],

#             'price': ['exact', 'gte', 'lte'],
#             'payment_status': ['exact', 'icontains'],
#             'delay_status': ['exact', 'icontains'],
#             'missed_month_substatus': ['exact', 'icontains'],
#             'incomplete_month_substatus': ['exact', 'icontains'],
#             'overpayment_substatus': ['exact', 'icontains'],
#             'contingent_payment_status': ['exact', 'icontains'],
#             'close_the_debt_status': ['exact', 'icontains'],
#         }

#     def contract_customer_fullname_filter(self, queryset, name, value):
#         qs = None
#         for term in value.split():
#             qs = Installment.objects.select_related('contract').filter(Q(contract__customer__first_name__icontains=term) | Q(
#                 contract__customer__last_name__icontains=term) | Q(
#                 contract__customer__father_name__icontains=term))
#         return qs

#     def contract_customer_phone_number_filter(self, queryset, name, value):
#         qs = None
#         for term in value.split():
#             qs = Installment.objects.select_related('contract').filter(
#                 Q(contract__customer__phone_number_1__icontains=term) | Q(contract__customer__phone_number_2__icontains=term) | Q(contract__customer__phone_number_3__icontains=term))
#         return qs
    
#     def contract__creditors__creditor_fullname_filter(self, queryset, name, value):
#         qs = None
#         for term in value.split():
#             qs = Installment.objects.filter(Q(contract__creditors__creditor__first_name__icontains=term) | Q(
#                 contract__creditors__creditor__last_name__icontains=term))
#         return qs


# class MuqavileFilter(django_filters.FilterSet):
#     contract_date = django_filters.DateFilter(
#         field_name='contract_date', input_formats=["%d-%m-%Y"])
#     contract_date__gte = django_filters.DateFilter(
#         field_name='contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     contract_date__lte = django_filters.DateFilter(
#         field_name='contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     contract_imzalanma_date = django_filters.DateFilter(
#         field_name='contract_imzalanma_date', input_formats=["%d-%m-%Y"])
#     contract_imzalanma_date__gte = django_filters.DateFilter(
#         field_name='contract_imzalanma_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     contract_imzalanma_date__lte = django_filters.DateFilter(
#         field_name='contract_imzalanma_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     negd_odenis_1_date = django_filters.DateFilter(
#         field_name='negd_odenis_1_date', input_formats=["%d-%m-%Y"])
#     negd_odenis_1_date__gte = django_filters.DateFilter(
#         field_name='negd_odenis_1_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     negd_odenis_1_date__lte = django_filters.DateFilter(
#         field_name='negd_odenis_1_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     negd_odenis_2_date = django_filters.DateFilter(
#         field_name='negd_odenis_2_date', input_formats=["%d-%m-%Y"])
#     negd_odenis_2_date__gte = django_filters.DateFilter(
#         field_name='negd_odenis_2_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     negd_odenis_2_date__lte = django_filters.DateFilter(
#         field_name='negd_odenis_2_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     initial_payment_date = django_filters.DateFilter(
#         field_name='initial_payment_date', input_formats=["%d-%m-%Y"])
#     initial_payment_date__gte = django_filters.DateFilter(
#         field_name='initial_payment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     initial_payment_date__lte = django_filters.DateFilter(
#         field_name='initial_payment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     initial_payment_debt_date = django_filters.DateFilter(
#         field_name='initial_payment_debt_date', input_formats=["%d-%m-%Y"])
#     initial_payment_debt_date__gte = django_filters.DateFilter(
#         field_name='initial_payment_debt_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     initial_payment_debt_date__lte = django_filters.DateFilter(
#         field_name='initial_payment_debt_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     class Meta:
#         model = Muqavile
#         fields = {
#             'customer__asa': ['exact', 'icontains'],
#             'customer__tel1': ['exact', 'icontains'],
#             'customer__tel2': ['exact', 'icontains'],
#             'customer__tel3': ['exact', 'icontains'],
#             'customer__tel4': ['exact', 'icontains'],
#             'customer__bolge__bolge_adi': ['exact', 'icontains'],
#             'customer__bolge': ['exact'],

#             'creditors__creditors__asa': ['exact'],
#             'creditors__creditors__id': ['exact'],

#             # 'contract_date': ['exact', 'gte', 'lte'],
#             # 'contract_imzalanma_date': ['exact', 'gte', 'lte'],

#             'company__id': ['exact'],
#             'company': ['exact'],
#             'company__name': ['exact', 'icontains'],
#             'office': ['exact'],
#             'office__id': ['exact'],
#             'office__name': ['exact', 'icontains'],

#             'payment_style': ['exact', 'icontains'],
#             'deyisilmis_mehsul_status': ['exact', 'icontains'],
#             'contract_status': ['exact', 'icontains'],

#             'negd_odenis_1': ['exact', 'gte', 'lte'],
#             'negd_odenis_2': ['exact', 'gte', 'lte'],
#             'negd_odenis_1_status': ['exact', 'icontains'],
#             'negd_odenis_2_status': ['exact', 'icontains'],
#             # 'negd_odenis_1_date': ['exact', 'gte', 'lte'],
#             # 'negd_odenis_2_date': ['exact', 'gte', 'lte'],

#             'yeni_qrafik_amount': ['exact', 'gte', 'lte'],
#             'yeni_qrafik_status': ['exact', 'icontains'],

#             'kredit_muddeti': ['exact', 'gte', 'lte'],

#             'initial_payment': ['exact', 'gte', 'lte'],
#             'initial_payment_debt': ['exact', 'gte', 'lte'],
#             # 'initial_payment_date': ['exact', 'gte', 'lte'],
#             # 'initial_payment_debt_date': ['exact', 'gte', 'lte'],
#             'initial_payment_status': ['exact', 'icontains'],
#             'residue_initial_payment_status': ['exact', 'icontains'],

#             'responsible_employee_1__team': ['exact'],
#             'responsible_employee_1__team__name': ['exact', 'icontains'],
#             'responsible_employee_1__asa': ['exact', 'icontains'],
#             'responsible_employee_1__employee_status__status_name': ['exact', 'icontains'],

#             'dealer__asa': ['exact', 'icontains'],
#             'dealer__employee_status__status_name': ['exact', 'icontains'],

#             'canvesser__asa': ['exact', 'icontains'],
#             'canvesser__employee_status__status_name': ['exact', 'icontains'],

#             'product_quantity': ['exact', 'gte', 'lte'],
#             'mehsul__mehsulun_adi': ['exact', 'icontains'],
#             'mehsul__price': ['exact', 'gte', 'lte'],

#             'total_amount': ['exact', 'gte', 'lte'],

#             'kompensasiya_income': ['exact', 'gte', 'lte'],
#             'kompensasiya_expense': ['exact', 'gte', 'lte'],

#             'is_sokuntu': ['exact']
#         }


# class MuqavileHediyyeFilter(django_filters.FilterSet):
#     contract__contract_date = django_filters.DateFilter(
#         field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
#     contract__contract_date__gte = django_filters.DateFilter(
#         field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     contract__contract_date__lte = django_filters.DateFilter(
#         field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     class Meta:
#         model = MuqavileHediyye
#         fields = {
#             'mehsul__id': ['exact'],
#             'mehsul__mehsulun_adi': ['exact', 'icontains'],
#             'mehsul__price': ['exact', 'gte', 'lte'],

#             'contract': ['exact'],
#             'contract__department__name': ['exact', 'icontains'],
#             'contract__office__name': ['exact', 'icontains'],
#             'contract__company__name': ['exact', 'icontains'],

#             'contract__responsible_employee_1__asa': ['exact', 'icontains'],
#             'contract__responsible_employee_1__team__name': ['exact', 'icontains'],
#             'contract__responsible_employee_1__employee_status__status_name': ['exact', 'icontains'],


#             'contract__payment_style': ['exact'],
#             'contract__contract_status': ['exact'],
#             # 'contract__contract_date': ['exact', 'gte', 'lte'],
#             'contract__total_amount': ['exact', 'gte', 'lte'],
#             'contract__product_quantity': ['exact', 'gte', 'lte'],

#             'contract__customer__asa': ['exact', 'icontains'],
#             'contract__customer__address': ['exact', 'icontains'],
#             'contract__customer__tel1': ['exact', 'icontains'],
#             'contract__customer__tel2': ['exact', 'icontains'],
#             'contract__customer__tel3': ['exact', 'icontains'],
#             'contract__customer__tel4': ['exact', 'icontains'],
#         }


# class DemoSatisFilter(django_filters.FilterSet):
#     created_date = django_filters.DateFilter(
#         field_name='created_date', input_formats=["%d-%m-%Y"])
#     created_date__gte = django_filters.DateFilter(
#         field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
#     created_date__lte = django_filters.DateFilter(
#         field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

#     class Meta:
#         model = DemoSatis
#         fields = {
#             'user': ['exact'],
#             'user__asa': ['exact'],
#             'user__company': ['exact'],
#             'user__company__name': ['exact', 'icontains'],
#             'user__office': ['exact'],
#             'user__office__name': ['exact', 'icontains'],
#             'user__vezife': ['exact'],
#             'user__vezife__vezife_adi': ['exact', 'icontains'],
#             'user__team': ['exact'],
#             'user__team__name': ['exact', 'icontains'],
#             # 'created_date': ['exact', 'gte', 'lte'],
#         }

import datetime

from celery import shared_task
import pandas as pd
from django.contrib.auth import get_user_model
from .models import DemoSales, Contract, Installment
from services.models import Service
from product.models import Product

User = get_user_model()

@shared_task(name='demo')
def demo_create_task():
    users = User.objects.all()

    now = datetime.date.today()
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        demos = DemoSales.objects.select_related("user").filter(
            user = user,
            created_date__year = next_m.year,
            created_date__month = next_m.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSales.objects.create(user=user, count=0, created_date=f"{next_m.year}-{next_m.month}-{1}").save()
    
    for user in users:
        demos = DemoSales.objects.select_related("user").filter(
            user = user,
            created_date__year = now.year,
            created_date__month = now.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSales.objects.create(user=user, count=0, created_date=f"{now.year}-{now.month}-{1}").save()

@shared_task(name='create_services_task')
def create_services_task(id):
    instance = Contract.objects.get(id=id)
    now = instance.contract_date

    d = pd.to_datetime(f"{now.year}-{now.month}-{now.day}")
    month6 = pd.date_range(start=d, periods=2, freq='6M')[1]
    month12 = pd.date_range(start=d, periods=2, freq='12M')[1]
    month18 = pd.date_range(start=d, periods=2, freq='18M')[1]
    month24 = pd.date_range(start=d, periods=2, freq='24M')[1]
    
    kartric6ay = Product.objects.select_related("company").filter(kartric_novu="KARTRIC6AY", company=instance.company)
    kartric12ay = Product.objects.select_related("company").filter(kartric_novu="KARTRIC12AY", company=instance.company)
    kartric18ay = Product.objects.select_related("company").filter(kartric_novu="KARTRIC18AY", company=instance.company)
    kartric24ay = Product.objects.select_related("company").filter(kartric_novu="KARTRIC24AY", company=instance.company)

    date_format = '%d-%m-%Y'
    kartric6ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month6.month}-{month6.year}", date_format)
    kartric6ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month6.day}-{month6.month}-{month6.year}", date_format)

    kartric12ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month12.month}-{month12.year}", date_format)
    kartric12ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month12.day}-{month12.month}-{month12.year}", date_format)

    kartric18ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month18.month}-{month18.year}", date_format)
    kartric18ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month18.day}-{month18.month}-{month18.year}", date_format)

    kartric24ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month24.month}-{month24.year}", date_format)
    kartric24ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month24.day}-{month24.month}-{month24.year}", date_format)

    q = 0
    while(q<instance.product_quantity):
        for i in range(1):
            price = 0
            for j in kartric6ay:
                price += float(j.price)
            if(now.day < 29):
                service = Service.objects.create(
                    contract=instance,
                    service_date = kartric6ay_date_lt_29,
                    price=price,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month6.day <= now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric6ay_date_eq_29_30_31,
                        price=price,
                        is_auto=True
                    )
                elif(month6.day > now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric6ay_date_lt_29,
                        price=price,
                        is_auto=True
                    )
            service.product.set(kartric6ay)
            service.save()
        for i in range(1):
            price = 0
            for j in kartric12ay:
                price += float(j.price)
            if(now.day < 29):
                service = Service.objects.create(
                    contract=instance,
                    service_date = kartric12ay_date_lt_29,
                    price=price,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month12.day <= now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric12ay_date_eq_29_30_31,
                        price=price,
                        is_auto=True
                    )
                elif(month12.day > now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric12ay_date_lt_29,
                        price=price,
                        is_auto=True
                    )
            service.product.set(kartric12ay)
            service.save()
        for i in range(1):
            price = 0
            for j in kartric18ay:
                price += float(j.price)
            if(now.day < 29):
                service = Service.objects.create(
                    contract=instance,
                    service_date = kartric18ay_date_lt_29,
                    price=price,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month18.day <= now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric18ay_date_eq_29_30_31,
                        price=price,
                        is_auto=True
                    )
                elif(month18.day > now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric18ay_date_lt_29,
                        price=price,
                        is_auto=True
                    )
            service.product.set(kartric18ay)
            service.save()
        for i in range(1):
            price = 0
            for j in kartric24ay:
                price += float(j.price)
            if(now.day < 29):
                service = Service.objects.create(
                    contract=instance,
                    service_date = kartric24ay_date_lt_29,
                    price=price,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month24.day <= now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric24ay_date_eq_29_30_31,
                        price=price,
                        is_auto=True
                    )
                elif(month24.day > now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date = kartric24ay_date_lt_29,
                        price=price,
                        is_auto=True
                    )
            service.product.set(kartric24ay)
            service.save()
        q+=1

@shared_task(name='create_installment_task')
def create_installment_task(id, created):
    instance = Contract.objects.get(id=id)
    loan_term = instance.loan_term
    product_quantity = instance.product_quantity

    if(instance.payment_style == "KREDİT"):
        # now = datetime.datetime.today().strftime('%d-%m-%Y')
        now = instance.contract_date
        inc_month = pd.date_range(now, periods = loan_term+1, freq='M')
        initial_payment = instance.initial_payment
        initial_payment_debt = instance.initial_payment_debt

        if(initial_payment is not None):
            initial_payment = float(initial_payment)
        
        if(initial_payment_debt is not None):
            initial_payment_debt = float(initial_payment_debt)

        total_amount = instance.total_amount
        if(initial_payment_debt == 0):
            initial_payment_total = initial_payment
        elif(initial_payment_debt != 0):
            initial_payment_total = initial_payment + initial_payment_debt
        total_payment_amount_for_month = total_amount - initial_payment_total
        
        if(loan_term > 0):
            payment_amount_for_month = total_payment_amount_for_month // loan_term

            debt = payment_amount_for_month * (loan_term - 1)
            payment_amount_for_last_month = total_payment_amount_for_month - debt

            if created:
                i = 1
                while(i<=loan_term):
                    if(i == loan_term):
                        if(now.day < 29):
                            Installment.objects.create(
                                month_no = i,
                                contract = instance,
                                date = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                                price = payment_amount_for_last_month,
                                last_month = True
                            ).save()
                        elif(now.day == 31 or now.day == 30 or now.day == 29):
                            if(inc_month[i].day <= now.day):
                                Installment.objects.create(
                                    month_no = i,
                                    contract = instance,
                                    date = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                    price = payment_amount_for_last_month,
                                    last_month = True
                                ).save()
                            elif(inc_month[i].day > now.day):
                                Installment.objects.create(
                                    month_no = i,
                                    contract = instance,
                                    date = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                                    price = payment_amount_for_last_month,
                                    last_month = True
                                ).save()
                    else:
                        if(now.day < 29):
                            Installment.objects.create(
                                month_no = i,
                                contract = instance,
                                date = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                                price = payment_amount_for_month
                            ).save()
                        elif(now.day == 31 or now.day == 30 or now.day == 29):
                            if(inc_month[i].day <= now.day):
                                Installment.objects.create(
                                    month_no = i,
                                    contract = instance,
                                    date = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                    price = payment_amount_for_month
                                ).save()
                            if(inc_month[i].day > now.day):
                                Installment.objects.create(
                                    month_no = i,
                                    contract = instance,
                                    date = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                                    price = payment_amount_for_month
                                ).save()
                    i+=1

@shared_task(name='demo_sale_count_task')
def demo_sale_count_task(id):
    instance = Contract.objects.get(id=id)
    responsible_employee_2 = instance.responsible_employee_2
    responsible_employee_3 = instance.responsible_employee_3
    contract_date = instance.contract_date
    product_quantity = instance.product_quantity
    sale_count = 0
    try:
        responsible_employee_2_demo = DemoSales.objects.select_related("user").filter(user=responsible_employee_2, created_date=contract_date)
        sale_count = sale_count + int(product_quantity)
        responsible_employee_2_demo.sale_count = sale_count
        responsible_employee_2_demo.save()
    except:
        sale_count = 0
    try:
        responsible_employee_3_demo = DemoSales.objects.select_related("user").filter(user=responsible_employee_3, created_date=contract_date)
        sale_count = sale_count + int(product_quantity)
        responsible_employee_3_demo.sale_count = sale_count
        responsible_employee_3_demo.save()
    except:
        sale_count = 0
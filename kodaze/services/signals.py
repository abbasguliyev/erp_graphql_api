# from contract.models import Contract
# from . models import Service, ServicePayment
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import datetime
# import pandas as pd

# from .tasks import create_services_task

# @receiver(post_save, sender=Contract)
# def create_services(sender, instance, created, **kwargs):
#     if created:
#         create_services_task.delay(instance.id)

# @receiver(post_save, sender=Service)
# def create_service_payment(sender, instance, created, **kwargs):
#     if created:
#         loan_term = instance.loan_term
#         installment = instance.installment
#         if int(loan_term) == 0:
#             loan_term = 1
#         print(f"****************************{loan_term=}")
#         print(f"****************************{installment=}")
#         discount = instance.discount
#         if discount == None:
#             discount = 0
        
#         initial_payment = instance.initial_payment
#         if initial_payment == None:
#             initial_payment = 0

#         price = instance.price
#         yekun = float(price) - float(initial_payment) - float(discount)
#         netice1 = yekun // loan_term
#         netice2 = netice1 * (loan_term - 1)
#         son_ay = yekun - netice2
#         # now_d = service_datei
#         # now = f"{now_d.year}-{now_d.month}-{1}"
        
#         now_d = instance.create_date
#         service_datei_str = instance.service_date
#         print(f"{service_datei_str=}")

#         # service_datei = pd.to_datetime(f"{service_datei_str.year}-{service_datei_str.month}-{service_datei_str.day}")
#         try:
#             service_datei = datetime.datetime.strptime(f"{service_datei_str.day}-{service_datei_str.month}-{service_datei_str.year}", '%d-%m-%Y')
#         except:
#             # service_datei = datetime.datetime.strptime(service_datei_str, '%d-%m-%Y')
#             service_datei = service_datei_str
#         inc_month = pd.date_range(service_datei, periods=loan_term+1, freq='M')

#         if installment == False:
#             service_payment = ServicePayment.objects.create(
#                                 service = instance,
#                                 total_amount_to_be_paid=yekun,
#                                 amount_to_be_paid=son_ay,
#                                 payment_date=f"{service_datei.year}-{service_datei.month}-{service_datei.day}"
#                             ).save()
#         elif installment == True:
#             j = 1
#             while(j<=int(loan_term)):
#                 if(j == int(loan_term)):
#                     if(service_datei.day < 29):
#                         service_payment = ServicePayment.objects.create(
#                             service = instance,
#                             total_amount_to_be_paid=yekun,
#                             amount_to_be_paid=son_ay,
#                             payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_datei.day}"
#                         ).save()
#                     elif(service_datei.day == 31 or service_datei.day == 30 or service_datei.day == 29):
#                         if(inc_month[j].day <= service_datei.day):
#                             service_payment = ServicePayment.objects.create(
#                                 service = instance,
#                                 total_amount_to_be_paid=yekun,
#                                 amount_to_be_paid=son_ay,
#                                 payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
#                             ).save()
#                         elif(inc_month[j].day > service_datei.day):
#                             service_payment = ServicePayment.objects.create(
#                                 service = instance,
#                                 total_amount_to_be_paid=yekun,
#                                 amount_to_be_paid=son_ay,
#                                 payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_datei.day}"
#                             ).save()
#                 else:
#                     if(service_datei.day < 29):
#                         service_payment = ServicePayment.objects.create(
#                             service = instance,
#                             total_amount_to_be_paid=yekun,
#                             amount_to_be_paid=netice1,
#                             payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_datei.day}"
#                         ).save()
#                     elif(service_datei.day == 31 or service_datei.day == 30 or service_datei.day == 29):
#                         if(inc_month[j].day <= service_datei.day):
#                             service_payment = ServicePayment.objects.create(
#                                 service = instance,
#                                 total_amount_to_be_paid=yekun,
#                                 amount_to_be_paid=netice1,
#                                 payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
#                             ).save()
#                         elif(inc_month[j].day > service_datei.day):
#                             service_payment = ServicePayment.objects.create(
#                                 service = instance,
#                                 total_amount_to_be_paid=yekun,
#                                 amount_to_be_paid=netice1,
#                                 payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_datei.day}"
#                             ).save()
#                 j += 1

from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import datetime

from account.models import User
from company.models import Position
from .models import CanvasserPrim, DealerPrimNew, SalaryView, OfficeLeaderPrim, VanLeaderPrimNew
from contract.models import Contract
import traceback

@receiver(post_save, sender=Contract)
def create_prim(sender, instance, created, **kwargs):
    if created:
        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        print(f"{now=}")
        print(f"{next_m=}")
        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        contract_loan_term = instance.loan_term
        contract_payment_style = instance.payment_style
        if contract_payment_style == "İKİ DƏFƏYƏ NƏĞD":
            contract_payment_style = "NƏĞD"

        responsible_employee_1 = instance.responsible_employee_1
        if responsible_employee_1 is not None:
            responsible_employee_1_status = responsible_employee_1.employee_status
        else:
            responsible_employee_1_status = None

        responsible_employee_2 = instance.responsible_employee_2
        if responsible_employee_2 is not None:
            responsible_employee_2_status = responsible_employee_2.employee_status
            responsible_employee_2_position = responsible_employee_2.position.name
        else:
            responsible_employee_2_status = None
            responsible_employee_2_position = None


        responsible_employee_3 = instance.responsible_employee_3
        if responsible_employee_3 is not None:
            responsible_employee_3_status = responsible_employee_3.employee_status
            responsible_employee_3_position = responsible_employee_3.position.name
        else:
            responsible_employee_3_status = None
            responsible_employee_3_position = None

        office = instance.office
        company = instance.company
        department = instance.responsible_employee_1.department
        print(f"{company=}")
        print(f"{department=}")
        if (office is not None) or (office != ""):
            officeLeaderPosition = Position.objects.get(name__icontains="OFFICE LEADER")
            officeLeaders = User.objects.filter(office=office, position=officeLeaderPosition)

            for officeLeader in officeLeaders:
                officeLeader_status = officeLeader.employee_status
                officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeaderPosition)

                officeLeader_salary_view_this_month = SalaryView.objects.get(employee=officeLeader, date=f"{now.year}-{now.month}-{1}")
                officeLeader_salary_view_novbeti_ay = SalaryView.objects.get(employee=officeLeader, date=f"{next_m.year}-{next_m.month}-{1}")

                officeLeader_salary_view_this_month.sales_quantity = float(officeLeader_salary_view_this_month.sales_quantity) + float(instance.product_quantity)
                officeLeader_salary_view_this_month.sales_amount = float(officeLeader_salary_view_this_month.sales_amount) + (float(instance.product.price) * float(instance.product_quantity))
                officeLeader_salary_view_this_month.save()

                officeLeader_salary_view_novbeti_ay.final_salary = float(officeLeader_salary_view_novbeti_ay.final_salary) + (float(officeleader_prim.prim_for_office) * float(instance.product_quantity))
                officeLeader_salary_view_novbeti_ay.save()

        # --------------------------------------------------------
        if (responsible_employee_1_status is not None):
            """
            Vanleaderin yeni uslubla salary hesablanmasi
            """
            responsible_employee_1_prim = VanLeaderPrimNew.objects.get(prim_status=responsible_employee_1_status, position=responsible_employee_1.position)
            
            responsible_employee_1_salary_view_this_month = SalaryView.objects.get(employee=responsible_employee_1, date=f"{now.year}-{now.month}-{1}")
            responsible_employee_1_salary_view_novbeti_ay = SalaryView.objects.get(employee=responsible_employee_1, date=next_m)

            responsible_employee_1_salary_view_this_month.sales_quantity = float(responsible_employee_1_salary_view_this_month.sales_quantity) + float(instance.product_quantity)
            responsible_employee_1_salary_view_this_month.sales_amount = float(responsible_employee_1_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            
            responsible_employee_1_salary_view_this_month.save()
            if contract_payment_style == "NƏĞD":
                responsible_employee_1_salary_view_novbeti_ay.final_salary = float(responsible_employee_1_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_1_prim.cash) * float(instance.product_quantity))
            elif contract_payment_style == "KREDİT":
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    responsible_employee_1_salary_view_novbeti_ay.final_salary = float(responsible_employee_1_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_1_prim.cash) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    responsible_employee_1_salary_view_novbeti_ay.final_salary = float(responsible_employee_1_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_1_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    responsible_employee_1_salary_view_novbeti_ay.final_salary = float(responsible_employee_1_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_1_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    responsible_employee_1_salary_view_novbeti_ay.final_salary = float(responsible_employee_1_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_1_prim.installment_19_24) * float(instance.product_quantity))

            responsible_employee_1_salary_view_novbeti_ay.save()
        
        # --------------------------------------------------------
        if (responsible_employee_2_position == "DEALER"):
            """
            Dealerin yeni uslubla salary hesablanmasi
            """
            responsible_employee_2_prim = DealerPrimNew.objects.get(prim_status=responsible_employee_2_status, position=responsible_employee_2.position)
            
            responsible_employee_2_salary_view_this_month = SalaryView.objects.get(employee=responsible_employee_2, date=f"{now.year}-{now.month}-{1}")
            responsible_employee_2_salary_view_novbeti_ay = SalaryView.objects.get(employee=responsible_employee_2, date=next_m)

            responsible_employee_2_salary_view_this_month.sales_quantity = float(responsible_employee_2_salary_view_this_month.sales_quantity) + float(instance.product_quantity)
            responsible_employee_2_salary_view_this_month.sales_amount = float(responsible_employee_2_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))

            responsible_employee_2_salary_view_this_month.save()

            if contract_payment_style == "NƏĞD":
                responsible_employee_2_salary_view_novbeti_ay.final_salary = float(responsible_employee_2_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_2_prim.cash) * float(instance.product_quantity))
            elif contract_payment_style == "KREDİT":
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    responsible_employee_2_salary_view_novbeti_ay.final_salary = float(responsible_employee_2_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_2_prim.cash) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    responsible_employee_2_salary_view_novbeti_ay.final_salary = float(responsible_employee_2_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_2_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    responsible_employee_2_salary_view_novbeti_ay.final_salary = float(responsible_employee_2_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_2_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    responsible_employee_2_salary_view_novbeti_ay.final_salary = float(responsible_employee_2_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_2_prim.installment_19_24) * float(instance.product_quantity))
            responsible_employee_2_salary_view_novbeti_ay.save()

        # --------------------------------------------------------
        if (responsible_employee_3_position == "CANVASSER"):
            responsible_employee_3_prim = CanvasserPrim.objects.get(prim_status=responsible_employee_3_status, position=responsible_employee_3.position)

            responsible_employee_3_salary_view_this_month = SalaryView.objects.get(employee=responsible_employee_3, date=f"{now.year}-{now.month}-{1}")
            responsible_employee_3_salary_view_novbeti_ay = SalaryView.objects.get(employee=responsible_employee_3, date=next_m)

            responsible_employee_3_salary_view_this_month.sales_quantity = float(responsible_employee_3_salary_view_this_month.sales_quantity) + float(instance.product_quantity)
            responsible_employee_3_salary_view_this_month.sales_amount = float(responsible_employee_3_salary_view_this_month.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            responsible_employee_3_salary_view_this_month.save()

            prim_for_sales_quantity = 0
            
            if (responsible_employee_3_salary_view_this_month.sales_quantity >= 9) and (responsible_employee_3_salary_view_this_month.sales_quantity <= 14):
                prim_for_sales_quantity = responsible_employee_3_prim.sale_9_14
            elif (responsible_employee_3_salary_view_this_month.sales_quantity >= 15):
                prim_for_sales_quantity = responsible_employee_3_prim.sale_15p
            elif (responsible_employee_3_salary_view_this_month.sales_quantity >= 20):
                prim_for_sales_quantity = responsible_employee_3_prim.sale_20p

            responsible_employee_3_salary_view_novbeti_ay.final_salary = float(responsible_employee_3_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_3_prim.prim_for_team) * float(instance.product_quantity)) + float(prim_for_sales_quantity)

            responsible_employee_3_salary_view_novbeti_ay.save()

        
        responsible_employee_3Position = Position.objects.get(name__icontains="CANVASSER")
        responsible_employee_3s = User.objects.filter(office=office, position=responsible_employee_3Position)

        for responsible_employee_3 in responsible_employee_3s:
            responsible_employee_3_status = responsible_employee_3.employee_status
            responsible_employee_3_prim = CanvasserPrim.objects.get(prim_status=responsible_employee_3_status, position=responsible_employee_3.position)

            responsible_employee_3_salary_view_novbeti_ay = SalaryView.objects.get(employee=responsible_employee_3, date=next_m)

            responsible_employee_3_salary_view_novbeti_ay.final_salary = float(responsible_employee_3_salary_view_novbeti_ay.final_salary) + (float(responsible_employee_3_prim.prim_for_office) * float(instance.product_quantity))

            responsible_employee_3_salary_view_novbeti_ay.save()
from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import datetime

from account.models import User
from company.models import Position
from .models import CanvasserPrim, DealerPrimNew, MaasGoruntuleme, OfficeLeaderPrim, VanLeaderPrimNew
from contract.models import Contract
import traceback

@receiver(post_save, sender=Contract)
def create_prim(sender, instance, created, **kwargs):
    if created:
        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        print(f"{indi=}")
        print(f"{next_m=}")
        days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month
        
        contract_loan_term = instance.loan_term
        contract_payment_style = instance.payment_style
        if contract_payment_style == "İKİ DƏFƏYƏ NƏĞD":
            contract_payment_style = "NƏĞD"

        person_in_charge_1 = instance.person_in_charge_1
        if person_in_charge_1 is not None:
            person_in_charge_1_status = person_in_charge_1.employee_status
        else:
            person_in_charge_1_status = None

        person_in_charge_2 = instance.person_in_charge_2
        if person_in_charge_2 is not None:
            person_in_charge_2_status = person_in_charge_2.employee_status
            person_in_charge_2_position = person_in_charge_2.position.name
        else:
            person_in_charge_2_status = None
            person_in_charge_2_position = None


        person_in_charge_3 = instance.person_in_charge_3
        if person_in_charge_3 is not None:
            person_in_charge_3_status = person_in_charge_3.employee_status
            person_in_charge_3_position = person_in_charge_3.position.name
        else:
            person_in_charge_3_status = None
            person_in_charge_3_position = None

        office = instance.office
        company = instance.company
        department = instance.person_in_charge_1.department
        print(f"{company=}")
        print(f"{department=}")
        if (office is not None) or (office != ""):
            officeLeaderPosition = Position.objects.get(name__icontains="OFFICE LEADER", company=company)
            officeLeaders = User.objects.filter(office=office, position=officeLeaderPosition)

            for officeLeader in officeLeaders:
                officeLeader_status = officeLeader.employee_status
                officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeaderPosition)

                officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=officeLeader, date=f"{indi.year}-{indi.month}-{1}")
                officeLeader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=officeLeader, date=f"{next_m.year}-{next_m.month}-{1}")

                officeLeader_maas_goruntulenme_bu_ay.satis_quantityi = float(officeLeader_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
                officeLeader_maas_goruntulenme_bu_ay.sales_amount = float(officeLeader_maas_goruntulenme_bu_ay.sales_amount) + (float(instance.product.price) * float(instance.product_quantity))
                officeLeader_maas_goruntulenme_bu_ay.save()

                officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas = float(officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(officeleader_prim.officee_gore_prim) * float(instance.product_quantity))
                officeLeader_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        # if (person_in_charge_1_status is not None):
        #     """
        #     Vanleaderin kohne uslubla salary hesablanmasi
        #     """
        #     person_in_charge_1_prim = VanLeaderPrim.objects.get(prim_status=person_in_charge_1_status, payment_style=contract_payment_style)
            
        #     person_in_charge_1_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_1, date=f"{indi.year}-{indi.month}-{1}")
        #     person_in_charge_1_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_1, date=next_m)

        #     person_in_charge_1_maas_goruntulenme_bu_ay.satis_quantityi = float(person_in_charge_1_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
        #     person_in_charge_1_maas_goruntulenme_bu_ay.sales_amount = float(person_in_charge_1_maas_goruntulenme_bu_ay.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))

        #     person_in_charge_1_maas_goruntulenme_bu_ay.save()

        #     person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.teamya_gore_prim) * float(instance.product_quantity))

        #     person_in_charge_1_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        if (person_in_charge_1_status is not None):
            """
            Vanleaderin yeni uslubla salary hesablanmasi
            """
            person_in_charge_1_prim = VanLeaderPrimNew.objects.get(prim_status=person_in_charge_1_status, position=person_in_charge_1.position)
            
            person_in_charge_1_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_1, date=f"{indi.year}-{indi.month}-{1}")
            person_in_charge_1_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_1, date=next_m)

            person_in_charge_1_maas_goruntulenme_bu_ay.satis_quantityi = float(person_in_charge_1_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
            person_in_charge_1_maas_goruntulenme_bu_ay.sales_amount = float(person_in_charge_1_maas_goruntulenme_bu_ay.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            
            person_in_charge_1_maas_goruntulenme_bu_ay.save()
            if contract_payment_style == "NƏĞD":
                person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.negd) * float(instance.product_quantity))
            elif contract_payment_style == "KREDİT":
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.negd) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_1_prim.installment_19_24) * float(instance.product_quantity))

            person_in_charge_1_maas_goruntulenme_novbeti_ay.save()
        # --------------------------------------------------------
        # if (person_in_charge_2_position == "DEALER"):
        #     person_in_charge_2_prim = DealerPrim.objects.get(prim_status=person_in_charge_2_status, payment_style=contract_payment_style)

        #     person_in_charge_2_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_2, date=f"{indi.year}-{indi.month}-{1}")
        #     person_in_charge_2_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_2, date=next_m)

        #     person_in_charge_2_maas_goruntulenme_bu_ay.satis_quantityi = float(person_in_charge_2_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
        #     person_in_charge_2_maas_goruntulenme_bu_ay.sales_amount = float(person_in_charge_2_maas_goruntulenme_bu_ay.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))

        #     person_in_charge_2_maas_goruntulenme_bu_ay.save()


        #     person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.teamya_gore_prim) * float(instance.product_quantity))

        #     person_in_charge_2_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (person_in_charge_2_position == "DEALER"):
            """
            Dealerin yeni uslubla salary hesablanmasi
            """
            person_in_charge_2_prim = DealerPrimNew.objects.get(prim_status=person_in_charge_2_status, position=person_in_charge_2.position)
            
            person_in_charge_2_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_2, date=f"{indi.year}-{indi.month}-{1}")
            person_in_charge_2_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_2, date=next_m)

            person_in_charge_2_maas_goruntulenme_bu_ay.satis_quantityi = float(person_in_charge_2_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
            person_in_charge_2_maas_goruntulenme_bu_ay.sales_amount = float(person_in_charge_2_maas_goruntulenme_bu_ay.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))

            person_in_charge_2_maas_goruntulenme_bu_ay.save()

            if contract_payment_style == "NƏĞD":
                person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.negd) * float(instance.product_quantity))
            elif contract_payment_style == "KREDİT":
                if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                    person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.negd) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                    person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.installment_4_12) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                    person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.installment_13_18) * float(instance.product_quantity))
                elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                    person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_2_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_2_prim.installment_19_24) * float(instance.product_quantity))
            person_in_charge_2_maas_goruntulenme_novbeti_ay.save()

        # --------------------------------------------------------
        if (person_in_charge_3_position == "CANVASSER"):
            person_in_charge_3_prim = CanvasserPrim.objects.get(prim_status=person_in_charge_3_status, position=person_in_charge_3.position)

            person_in_charge_3_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_3, date=f"{indi.year}-{indi.month}-{1}")
            person_in_charge_3_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_3, date=next_m)

            person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi = float(person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi) + float(instance.product_quantity)
            person_in_charge_3_maas_goruntulenme_bu_ay.sales_amount = float(person_in_charge_3_maas_goruntulenme_bu_ay.sales_amount) +  (float(instance.product.price) * float(instance.product_quantity))
            person_in_charge_3_maas_goruntulenme_bu_ay.save()

            satis_quantityina_gore_prim = 0
            
            if (person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi >= 9) and (person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi <= 14):
                satis_quantityina_gore_prim = person_in_charge_3_prim.satis9_14
            elif (person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi >= 15):
                satis_quantityina_gore_prim = person_in_charge_3_prim.satis15p
            elif (person_in_charge_3_maas_goruntulenme_bu_ay.satis_quantityi >= 20):
                satis_quantityina_gore_prim = person_in_charge_3_prim.satis20p

            person_in_charge_3_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_3_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_3_prim.teamya_gore_prim) * float(instance.product_quantity)) + float(satis_quantityina_gore_prim)

            person_in_charge_3_maas_goruntulenme_novbeti_ay.save()

        
        person_in_charge_3Position = Position.objects.get(name__icontains="CANVASSER", company=company)
        person_in_charge_3s = User.objects.filter(office=office, position=person_in_charge_3Position)

        for person_in_charge_3 in person_in_charge_3s:
            person_in_charge_3_status = person_in_charge_3.employee_status
            person_in_charge_3_prim = CanvasserPrim.objects.get(prim_status=person_in_charge_3_status, position=person_in_charge_3.position)

            person_in_charge_3_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_3, date=next_m)

            person_in_charge_3_maas_goruntulenme_novbeti_ay.yekun_maas = float(person_in_charge_3_maas_goruntulenme_novbeti_ay.yekun_maas) + (float(person_in_charge_3_prim.officee_gore_prim) * float(instance.product_quantity))

            person_in_charge_3_maas_goruntulenme_novbeti_ay.save()
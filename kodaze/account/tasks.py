import datetime
from company.models import Position
from .models import User
from celery import shared_task
import pandas as pd
from salary.models import CanvasserPrim, MaasGoruntuleme, OfficeLeaderPrim, VanLeaderPrim



@shared_task(name='maas_goruntuleme_create_task')
def maas_goruntuleme_create_task():
    users = User.objects.all()
    indi = datetime.date.today()
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        employee_maas = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(employee_maas) != 0:
            continue
        else:
            if user.salary_style == "FİX": 
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}").save()

    for user in users:
        employee_maas = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_maas) != 0:
            continue
        else:
            if user.salary_style == "FİX": 
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}").save()

@shared_task(name='maas_goruntuleme_create_task_15')
def maas_goruntuleme_create_task_15():
    users = User.objects.all()
    indi = datetime.date.today()
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        employee_maas = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = next_m.year,
            tarix__month = next_m.month
        )
        if len(employee_maas) != 0:
            continue
        else:
            if user.salary_style == "FİX": 
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}").save()

    for user in users:
        employee_maas = MaasGoruntuleme.objects.filter(
            employee=user, 
            tarix__year = indi.year,
            tarix__month = indi.month
        )
        if len(employee_maas) != 0:
            continue
        else:
            if user.salary_style == "FİX": 
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}", yekun_maas=user.salary).save()
            else:    
                MaasGoruntuleme.objects.create(employee=user, date=f"{indi.year}-{indi.month}-{1}").save()


@shared_task(name='employee_fix_maas_auto_elave_et')
def employee_fix_maas_auto_elave_et():
    indi = datetime.date.today()

    bu_ay = f"{indi.year}-{indi.month}-{1}"
    
    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    evvelki_ay = d - pd.offsets.MonthBegin(1)

    officeLeaderPosition = Position.objects.filter(name="OFFICE LEADER")[0]
    officeLeaders = User.objects.filter(position__name=officeLeaderPosition.name)

    for officeLeader in officeLeaders:
        officeLeader_status = officeLeader.employee_status

        officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeader.position)
        officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=officeLeader, date=bu_ay)

        officeLeader_maas_goruntulenme_bu_ay.yekun_maas = float(officeLeader_maas_goruntulenme_bu_ay.yekun_maas) + float(officeleader_prim.fix_maas)
        officeLeader_maas_goruntulenme_bu_ay.save()
    
    # vanLeaderPosition = Position.objects.get(name="VAN LEADER")
    # vanLeaders = User.objects.filter(position=vanLeaderPosition)

    # for person_in_charge_1 in vanLeaders:
    #     person_in_charge_1_status = person_in_charge_1.employee_status

    #     person_in_charge_1_prim = VanLeaderPrim.objects.get(prim_status=person_in_charge_1_status, payment_style="NƏĞD")

    #     person_in_charge_1_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_1, date=bu_ay)

    #     person_in_charge_1_maas_goruntulenme_bu_ay.yekun_maas = float(person_in_charge_1_maas_goruntulenme_bu_ay.yekun_maas) + float(person_in_charge_1_prim.fix_maas)
    #     person_in_charge_1_maas_goruntulenme_bu_ay.save()

    canvasserPosition = Position.objects.filter(name="CANVASSER")[0]
    canvassers = User.objects.filter(position__name=canvasserPosition.name)

    for person_in_charge_3 in canvassers:
        person_in_charge_3_status = person_in_charge_3.employee_status

        person_in_charge_3_prim = CanvasserPrim.objects.get(prim_status=person_in_charge_3_status, position=person_in_charge_3.position)

        person_in_charge_3_maas_goruntulenme_evvelki_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_3, date=evvelki_ay)
        person_in_charge_3_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(employee=person_in_charge_3, date=f"{indi.year}-{indi.month}-{1}")

        satis_quantityina_gore_prim = 0
        if (person_in_charge_3_maas_goruntulenme_evvelki_ay.satis_quantityi == 0):
            satis_quantityina_gore_prim = person_in_charge_3_prim.satis0
        elif (person_in_charge_3_maas_goruntulenme_evvelki_ay.satis_quantityi >= 1) and (person_in_charge_3_maas_goruntulenme_evvelki_ay.satis_quantityi <= 8):
            satis_quantityina_gore_prim = person_in_charge_3_prim.satis1_8

        person_in_charge_3_maas_goruntulenme_bu_ay.yekun_maas = float(person_in_charge_3_maas_goruntulenme_bu_ay.yekun_maas) + float(satis_quantityina_gore_prim) + float(person_in_charge_3_prim.fix_maas)
        person_in_charge_3_maas_goruntulenme_bu_ay.save()
        person_in_charge_3_maas_goruntulenme_evvelki_ay.save()
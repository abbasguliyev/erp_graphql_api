import traceback
from cashbox.models import OfficeCashbox
from contract.models import  Installment
from rest_framework.exceptions import ValidationError
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
import pandas as pd
import django

from restAPI.v1.cashbox.utils import (
    holding_umumi_balance_hesabla, 
    pul_axini_create, 
    ofis_balance_hesabla
)

from restAPI.v1.contract.utils.muqavile_utils import (
    c_income, 
    expense,
    pdf_create_when_muqavile_updated
)

# PATCH sorgusu
def installment_patch(self, request, *args, **kwargs):
    pass

# UPDATE SORGUSU
def installment_update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    odenme_status = request.data.get("odenme_status")
    sertli_odeme_status = request.data.get("sertli_odeme_status")
    gecikdirme_status = request.data.get("gecikdirme_status")
    natamama_gore_odeme_status = request.data.get("natamam_ay_alt_status")
    sifira_gore_odeme_status = request.data.get("buraxilmis_ay_alt_status")
    artiq_odeme_alt_status = request.data.get('artiq_odeme_alt_status')

    user = request.user

    now_ay = self.get_object()
    odemek_istediyi_amount = request.data.get("price")

    if odemek_istediyi_amount == None:
        odemek_istediyi_amount = 0

    today = datetime.date.today()

    muqavile = now_ay.muqavile
    responsible_employee_1 = muqavile.responsible_employee_1
    musteri = muqavile.musteri
    payment_style = muqavile.payment_style
    ofis = muqavile.ofis

    ofis_cashbox = get_object_or_404(OfficeCashbox, ofis=ofis)

    borcu_bagla_status = request.data.get("borcu_bagla_status")

    residue_borc = muqavile.residue_borc

    note = request.data.get("note")
    if note == None:
        note = ""

    def umumi_amount(mehsul_pricei, product_quantity):
        muqavile_umumi_amount = mehsul_pricei * product_quantity
        return muqavile_umumi_amount
    
    # BORCU BAĞLA ILE BAGLI EMELIYYATLAR
    if(borcu_bagla_status == "BORCU BAĞLA"):
        odenmeyen_odemedateler_qs = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemedateler = list(odenmeyen_odemedateler_qs)

        ay_ucun_olan_amount = 0
        for i in odenmeyen_odemedateler:
            ay_ucun_olan_amount = ay_ucun_olan_amount + float(i.price)
            # i.price = 0
            # i.odenme_status = "ÖDƏNƏN"
            # i.note = note
            # i.save()
            i.delete()

        now_ay.price = residue_borc
        now_ay.odenme_status = "ÖDƏNƏN"
        now_ay.save()

        muqavile.muqavile_status = "BİTMİŞ"
        muqavile.borc_baglanma_date = django.utils.timezone.now()
        residue_borc = 0
        muqavile.residue_borc = residue_borc
        muqavile.borc_baglandi = True
        muqavile.save()

        ilkin_balance = holding_umumi_balance_hesabla()
        print(f"{ilkin_balance=}")
        ofis_ilkin_balance = ofis_balance_hesabla(ofis=ofis)

        note = f"Vanleader - {responsible_employee_1.asa}, müştəri - {musteri.asa}, date - {today}, ödəniş üslubu - {payment_style}. Borcu tam bağlandı"
        c_income(ofis_cashbox, float(ay_ucun_olan_amount), responsible_employee_1, note)

        sonraki_balance = holding_umumi_balance_hesabla()
        print(f"{sonraki_balance=}")
        ofis_sonraki_balance = ofis_balance_hesabla(ofis=ofis)
        pul_axini_create(
            ofis=ofis,
            shirket=ofis.shirket,
            aciqlama=note,
            ilkin_balance=ilkin_balance,
            sonraki_balance=sonraki_balance,
            ofis_ilkin_balance=ofis_ilkin_balance,
            ofis_sonraki_balance=ofis_sonraki_balance,
            emeliyyat_eden=user,
            emeliyyat_uslubu="MƏDAXİL",
            miqdar=float(ay_ucun_olan_amount)
        )

        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Borc tam bağlandı"}, status=status.HTTP_200_OK)

    # GECIKDIRME ILE BAGLI EMELIYYATLAR
    if(
        (now_ay.odenme_status == "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ")  
        or 
        (now_ay.odenme_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None) 
        or 
        (odenme_status == "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ") 
        or 
        (odenme_status == "ÖDƏNMƏYƏN" and request.data.get("date") is not None)
    ):
        my_time = datetime.datetime.min.time()

        installment_date = now_ay.date
        installment = datetime.datetime.combine(installment_date, my_time)
        installment_san = datetime.datetime.timestamp(installment)

        gecikdirmek_istediyi_date = request.data.get("date")
        gecikdirmek_istediyi_date_date = datetime.datetime.strptime(gecikdirmek_istediyi_date, "%d-%m-%Y")
        gecikdirmek_istediyi_date_san = datetime.datetime.timestamp(gecikdirmek_istediyi_date_date)

        odenmeyen_odemedateler_qs = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemedateler = list(odenmeyen_odemedateler_qs)

        if(now_ay == odenmeyen_odemedateler[-1]):
            try:
                if(gecikdirmek_istediyi_date_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date keçmiş datedir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(installment_san < gecikdirmek_istediyi_date_san):
                    now_ay.date = gecikdirmek_istediyi_date
                    now_ay.gecikdirme_status = "GECİKDİRMƏ"
                    # now_ay.note = note
                    now_ay.save()
                    pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni date hal-hazırki date ile növbəti ayın date arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        elif(now_ay != odenmeyen_odemedateler[-1]):
            novbeti_ay = Installment.objects.get(pk = now_ay.id+1)
            novbeti_ay_date_date = novbeti_ay.date
            novbeti_ay_date = datetime.datetime.combine(novbeti_ay_date_date, my_time)
            novbeti_ay_date_san = datetime.datetime.timestamp(novbeti_ay_date)

            try:
                if(novbeti_ay_date_san == gecikdirmek_istediyi_date_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date növbəti ayın date ilə eynidir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_date_san < installment_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date keçmiş datedir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_date_san > novbeti_ay_date_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz date növbəti ayın datendən böyükdür."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(installment_san < gecikdirmek_istediyi_date_san < novbeti_ay_date_san):
                    now_ay.date = gecikdirmek_istediyi_date
                    now_ay.gecikdirme_status = "GECİKDİRMƏ"
                    # now_ay.note = note
                    now_ay.save()
                    pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni date hal-hazırki date ile növbəti ayın date arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
    elif(now_ay.odenme_status != "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ"):
        raise ValidationError(detail={"detail": "Gecikdirmə ancaq ödənməmiş ay üçündür"}, code=status.HTTP_400_BAD_REQUEST)
    
    # Natamam Ay odeme statusu ile bagli emeliyyatlar
    if(
        now_ay.odenme_status == "ÖDƏNMƏYƏN" 
        and 
        sertli_odeme_status == "NATAMAM AY" 
        and 
        0 < float(odemek_istediyi_amount) < now_ay.price 
        and 
        natamama_gore_odeme_status != ""
        and 
        natamama_gore_odeme_status is not None
    ):
        initial_payment = muqavile.initial_payment
        initial_payment_debt = muqavile.initial_payment_debt
        initial_payment_full = initial_payment + initial_payment_debt
        total_amount = muqavile.muqavile_umumi_amount
        now_ay.odenme_status = "ÖDƏNƏN"
        now_ay.sertli_odeme_status = "NATAMAM AY"
        # now_ay.note = note
        now_ay.save()


        odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
        odemek_istediyi_amount = float(request.data.get("price"))
        
        ilkin_balance = holding_umumi_balance_hesabla()
        print(f"{ilkin_balance=}")
        ofis_ilkin_balance = ofis_balance_hesabla(ofis=ofis)

        note = f"Vanleader - {responsible_employee_1.asa}, müştəri - {musteri.asa}, date - {today}, ödəniş üslubu - {payment_style}, şərtli ödəmə - {now_ay.sertli_odeme_status}"
        c_income(ofis_cashbox, float(odemek_istediyi_amount), responsible_employee_1, note)
        residue_borc = muqavile.residue_borc
        residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
        muqavile.residue_borc = residue_borc
        muqavile.save()

        sonraki_balance = holding_umumi_balance_hesabla()
        print(f"{sonraki_balance=}")
        ofis_sonraki_balance = ofis_balance_hesabla(ofis=ofis)
        pul_axini_create(
            ofis=ofis,
            shirket=ofis.shirket,
            aciqlama=note,
            ilkin_balance=ilkin_balance,
            sonraki_balance=sonraki_balance,
            ofis_ilkin_balance=ofis_ilkin_balance,
            ofis_sonraki_balance=ofis_sonraki_balance,
            emeliyyat_eden=user,
            emeliyyat_uslubu="MƏDAXİL",
            miqdar=float(odemek_istediyi_amount)
        )
        
        if(natamama_gore_odeme_status == "NATAMAM DİGƏR AYLAR"):
            odenmeyen_pul = now_ay.price - odemek_istediyi_amount
            odenmeyen_aylar = len(odenmeyen_odemedateler)

            buraxilmamis_odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
            
            aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            b = aylara_elave_olunacaq_amount * (odenmeyen_aylar - 1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - b
            
            now_ay.price = odemek_istediyi_amount
            now_ay.natamam_ay_alt_status = "NATAMAM DİGƏR AYLAR"
            now_ay.odenme_status = "ÖDƏNƏN"
            # now_ay.note = note
            now_ay.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(now_ay == buraxilmamis_odenmeyen_odemedateler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    odenmeyen_odemedateler[i].price = odenmeyen_odemedateler[i].price + last_montha_elave_olunacaq_amount
                    odenmeyen_odemedateler[i].save()
                else:
                    odenmeyen_odemedateler[i].price = odenmeyen_odemedateler[i].price + aylara_elave_olunacaq_amount
                    odenmeyen_odemedateler[i].save()
                i+=1
            if serializer.is_valid():
                serializer.save(odenme_status = "ÖDƏNƏN")
                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM NÖVBƏTİ AY"):
            now_ay = self.get_object()
            natamam_odemek_istediyi_amount = now_ay.price - odemek_istediyi_amount

            novbeti_ay = get_object_or_404(Installment, pk=self.get_object().id+1)
            novbeti_ay.price = novbeti_ay.price + natamam_odemek_istediyi_amount
            novbeti_ay.save()

            now_ay.price = odemek_istediyi_amount
            now_ay.natamam_ay_alt_status = "NATAMAM NÖVBƏTİ AY"
            now_ay.odenme_status = "ÖDƏNƏN"
            # now_ay.note = note
            now_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM SONUNCU AY"):
            now_ay = self.get_object()
            natamam_odemek_istediyi_amount = now_ay.price - odemek_istediyi_amount

            last_month = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1]
            last_month.price = last_month.price + natamam_odemek_istediyi_amount
            last_month.save()

            now_ay.price = odemek_istediyi_amount
            now_ay.natamam_ay_alt_status = "NATAMAM SONUNCU AY"
            now_ay.odenme_status = "ÖDƏNƏN"
            # now_ay.note = note
            now_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        
    # Buraxilmis Ay odeme statusu ile bagli emeliyyatlar
    if((sertli_odeme_status == "BURAXILMIŞ AY" and sifira_gore_odeme_status != None) or (float(odemek_istediyi_amount) == 0 and sifira_gore_odeme_status != None)):
        now_ay = self.get_object()
        muqavile = now_ay.muqavile
        initial_payment = muqavile.initial_payment
        initial_payment_debt = muqavile.initial_payment_debt
        total_amount = muqavile.muqavile_umumi_amount
        initial_payment_full = initial_payment + initial_payment_debt
        # now_ay.sertli_odeme_status = "BURAXILMIŞ AY"
        # now_ay.save()
        odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
        odemek_istediyi_amount = float(request.data.get("price"))
        
        if(sifira_gore_odeme_status == "SIFIR NÖVBƏTİ AY"):
            novbeti_ay = get_object_or_404(Installment, pk=self.get_object().id+1)
            novbeti_ay.price = novbeti_ay.price + now_ay.price
            novbeti_ay.save()
            now_ay.price = 0
            now_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            now_ay.buraxilmis_ay_alt_status = "SIFIR NÖVBƏTİ AY"
            # now_ay.note = note
            now_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR SONUNCU AY"):
            last_month = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1]
            last_month.price = last_month.price + now_ay.price
            last_month.save()
            now_ay.price = 0
            now_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            now_ay.buraxilmis_ay_alt_status = "SIFIR SONUNCU AY"
            # now_ay.note = note
            now_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR DİGƏR AYLAR"):
            odenmeyen_pul = now_ay.price
            buraxilmamis_odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_odemedateler)
            aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            a = aylara_elave_olunacaq_amount * ((odenmeyen_aylar - 1)-1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - a
            now_ay.price = 0
            now_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            now_ay.buraxilmis_ay_alt_status = "SIFIR DİGƏR AYLAR"
            # now_ay.note = note
            now_ay.save()
            i = 0
            
            while(i<=(odenmeyen_aylar-1)):
                if(now_ay == buraxilmamis_odenmeyen_odemedateler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_odemedateler[i].price = buraxilmamis_odenmeyen_odemedateler[i].price + last_montha_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_odemedateler[i].save()
                else:
                    buraxilmamis_odenmeyen_odemedateler[i].price = buraxilmamis_odenmeyen_odemedateler[i].price + aylara_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_odemedateler[i].save()
                i+=1
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # RAZILASDIRILMIS AZ ODEME ile bagli emeliyyatlar
    if(sertli_odeme_status == "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"):
        odemek_istediyi_amount = float(request.data.get("price"))
        if float(now_ay.price) <= float(odemek_istediyi_amount):
            return Response({"detail": "Razılaşdırılmış ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən az olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            now_ay = self.get_object()
            muqavile = now_ay.muqavile
            buraxilmamis_odenmeyen_odemedateler = Installment.objects.filter(
                muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", buraxilmis_ay_alt_status=None, sertli_odeme_status=None 
                )
            initial_payment = muqavile.initial_payment
            initial_payment_debt = muqavile.initial_payment_debt
            initial_payment_full = initial_payment + initial_payment_debt
            total_amount = muqavile.muqavile_umumi_amount
            now_ay.sertli_odeme_status = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
            # now_ay.note = note
            now_ay.save()

            # odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        
            odenmeyen_pul = now_ay.price - odemek_istediyi_amount
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_odemedateler)
            
            try:
                aylara_elave_olunacaq_amount = odenmeyen_pul // (odenmeyen_aylar - 1)
            except ZeroDivisionError:
                aylara_elave_olunacaq_amount = odenmeyen_pul // odenmeyen_aylar
            if(now_ay.odenme_status=="ÖDƏNƏN"):
                b = aylara_elave_olunacaq_amount * ((odenmeyen_aylar-1)-1)
            elif(now_ay.odenme_status=="ÖDƏNMƏYƏN"):
                b = aylara_elave_olunacaq_amount * ((odenmeyen_aylar)-1)
            last_montha_elave_olunacaq_amount = odenmeyen_pul - b
            
            now_ay.odenme_status = "ÖDƏNMƏYƏN"
            now_ay.price = odemek_istediyi_amount
            now_ay.save()

            residue_borc = float(residue_borc) - float(now_ay.price)
            # muqavile.residue_borc = residue_borc
            muqavile.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(now_ay == buraxilmamis_odenmeyen_odemedateler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_odemedateler[i].price = buraxilmamis_odenmeyen_odemedateler[i].price + last_montha_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_odemedateler[i].save()
                else:
                    buraxilmamis_odenmeyen_odemedateler[i].price = buraxilmamis_odenmeyen_odemedateler[i].price + aylara_elave_olunacaq_amount
                    buraxilmamis_odenmeyen_odemedateler[i].save()
                i+=1
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # ARTIQ ODEME ile bagli emeliyyatlar
    if(sertli_odeme_status == "ARTIQ ÖDƏMƏ"):
        odenmek_istenilen_amount = request.data.get("price")
        
        if float(now_ay.price) >= float(odenmek_istenilen_amount):
            return Response({"detail": "Artıq ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən çox olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(artiq_odeme_alt_status == "ARTIQ BİR AY"):
                now_ay = self.get_object()
                muqavile = now_ay.muqavile
                odemek_istediyi_amount = float(request.data.get("price"))
                normalda_odenmeli_olan = now_ay.price

                if float(odemek_istediyi_amount) > float(muqavile.residue_borc):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                artiqdan_normalda_odenmeli_olani_cixan_ferq = odemek_istediyi_amount - normalda_odenmeli_olan
                print(f"{artiqdan_normalda_odenmeli_olani_cixan_ferq=}")
                odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")

                now_ay.price = odemek_istediyi_amount
                now_ay.sertli_odeme_status = "ARTIQ ÖDƏMƏ"
                now_ay.artiq_odeme_alt_status = "ARTIQ BİR AY"
                now_ay.save()
                
                residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
                muqavile.save()

                last_month = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1]
                sonuncudan_bir_evvelki_ay = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-2]
                
                last_monthdan_qalan = last_month.price - artiqdan_normalda_odenmeli_olani_cixan_ferq
                while(artiqdan_normalda_odenmeli_olani_cixan_ferq>0):
                    if(last_month.price > artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        print(f"1")
                        last_month.price = last_month.price - artiqdan_normalda_odenmeli_olani_cixan_ferq
                        last_month.save()
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = 0
                        print(f"{artiqdan_normalda_odenmeli_olani_cixan_ferq=}")

                    elif(last_month.price == artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        print(f"2")
                        last_month.delete()
                        muqavile.kredit_muddeti = muqavile.kredit_muddeti - 1
                        muqavile.save()
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = 0
                        print(f"{artiqdan_normalda_odenmeli_olani_cixan_ferq=}")
                    elif(last_month.price < artiqdan_normalda_odenmeli_olani_cixan_ferq):
                        print(f"3")
                        artiqdan_normalda_odenmeli_olani_cixan_ferq = artiqdan_normalda_odenmeli_olani_cixan_ferq - last_month.price
                        print(f"{artiqdan_normalda_odenmeli_olani_cixan_ferq=}")
                        last_month.delete()
                        muqavile.kredit_muddeti = muqavile.kredit_muddeti - 1
                        muqavile.save()
                        odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
                        last_month = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1]
                        sonuncudan_bir_evvelki_ay = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-2]
                        print(f"{last_month.price=}")
                        print(f"{sonuncudan_bir_evvelki_ay.price=}")

                if(request.data.get("odenme_status") == "ÖDƏNƏN"):
                    residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
                    muqavile.residue_borc = residue_borc
                    muqavile.save()

                    ilkin_balance = holding_umumi_balance_hesabla()
                    print(f"{ilkin_balance=}")
                    ofis_ilkin_balance = ofis_balance_hesabla(ofis=ofis)
                    
                    note = f"Vanleader - {responsible_employee_1.asa}, müştəri - {musteri.asa}, date - {today}, ödəniş üslubu - {payment_style}. kredit ödəməsi"
                    c_income(ofis_cashbox, float(odemek_istediyi_amount), responsible_employee_1, note)

                    now_ay.odenme_status = "ÖDƏNƏN"
                    now_ay.save()

                    sonraki_balance = holding_umumi_balance_hesabla()
                    print(f"{sonraki_balance=}")
                    ofis_sonraki_balance = ofis_balance_hesabla(ofis=ofis)
                    pul_axini_create(
                        ofis=ofis,
                        shirket=ofis.shirket,
                        aciqlama=note,
                        ilkin_balance=ilkin_balance,
                        sonraki_balance=sonraki_balance,
                        ofis_ilkin_balance=ofis_ilkin_balance,
                        ofis_sonraki_balance=ofis_sonraki_balance,
                        emeliyyat_eden=user,
                        emeliyyat_uslubu="MƏDAXİL",
                        miqdar=float(odemek_istediyi_amount)
                    )


                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            elif(artiq_odeme_alt_status == "ARTIQ BÜTÜN AYLAR"):
                now_ay = self.get_object()
                muqavile = now_ay.muqavile
                odemek_istediyi_amount = float(request.data.get("price"))
                print(f"{odemek_istediyi_amount=}")
                normalda_odenmeli_olan = now_ay.price

                if float(odemek_istediyi_amount) > float(muqavile.residue_borc):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                initial_payment = muqavile.initial_payment
                initial_payment_debt = muqavile.initial_payment_debt
                initial_payment_full = initial_payment + initial_payment_debt
                total_amount = muqavile.muqavile_umumi_amount
                odenen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status = "ÖDƏNƏN")
                odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
                umumi_odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status="BURAXILMIŞ AY")
                sertli_odeme = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status=None)
                print(f"******************************{odenmeyen_odemedateler=} ---> {len(odenmeyen_odemedateler)}")
                print(f"******************************{umumi_odenmeyen_odemedateler=} ---> {len(umumi_odenmeyen_odemedateler)}")
                print(f"******************{sertli_odeme=}")

                sertli_odemeden_gelen_amount = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_amount += float(s.price)
                print(f"******************{sertli_odemeden_gelen_amount=}")
                installmentleri = Installment.objects.filter(muqavile=muqavile)
                # odediyi = len(odenen_odemedateler) * now_ay.price
                residue_borc = float(muqavile.residue_borc)
                print(f"******************{residue_borc=}")
                yeni_residue_borc = residue_borc-sertli_odemeden_gelen_amount
                print(f"******************{yeni_residue_borc=}")
                # cixilacaq_amount = residue_borc -  sertli_odemeden_gelen_amount
                yeni_aylar = yeni_residue_borc // odemek_istediyi_amount
                print(f"******************{yeni_aylar=}")
                # silinecek_ay = len(odenmeyen_odemedateler) - yeni_aylar
                silinecek_ay = len(umumi_odenmeyen_odemedateler) - yeni_aylar - len(sertli_odeme)
                print(f"******************{silinecek_ay=}")
                son_aya_elave_edilecek_amount = yeni_residue_borc - ((yeni_aylar-1) * odemek_istediyi_amount)
                print(f"******************{son_aya_elave_edilecek_amount=}")
                now_ay.price = odemek_istediyi_amount
                # now_ay.odenme_status = "ÖDƏNƏN"
                now_ay.sertli_odeme_status = "ARTIQ ÖDƏMƏ"
                now_ay.artiq_odeme_alt_status = "ARTIQ BÜTÜN AYLAR"
                # now_ay.note = note
                now_ay.save()

                residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
                # muqavile.residue_borc = residue_borc
                muqavile.save()

                a = 1
                while(a <= silinecek_ay):
                    odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1].delete()
                    odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
                    a += 1

                print(f"********Silinmeden sonra***********{odenmeyen_odemedateler=} ---> {len(odenmeyen_odemedateler)}")

                b = 0
                if float(odemek_istediyi_amount) == float(residue_borc):
                    while(b < yeni_aylar):
                        print(f"******************{b=}")
                        odenmeyen_odemedateler[b].price = odemek_istediyi_amount
                        odenmeyen_odemedateler[b].save()
                        b += 1
                elif float(odemek_istediyi_amount) < float(residue_borc):
                    while(b < yeni_aylar):
                        print(f"******************{b=}")
                        if(b < yeni_aylar-1):
                            installment = odenmeyen_odemedateler[b]
                            installment.price = odemek_istediyi_amount
                            installment.save()
                            b += 1
                        elif(b == yeni_aylar-1):
                            odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1].price = son_aya_elave_edilecek_amount
                            odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1].save()
                            b += 1
                        
                # serializer.save()
                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    
    # SON AYIN BOLUNMESI
    if(sertli_odeme_status == "SON AYIN BÖLÜNMƏSİ"):
        now_ay = self.get_object()
        muqavile = now_ay.muqavile
        odemek_istediyi_amount = float(request.data.get("price"))

        if float(odemek_istediyi_amount) == 0:
            return Response({"detail": "Sonuncu ayda 0 AZN daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        odenmeyen_odemedateler = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        last_month = odenmeyen_odemedateler[len(odenmeyen_odemedateler)-1]

        try:
            if(now_ay != last_month):
                raise ValidationError(detail={"detail": "Sonuncu ayda deyilsiniz!"}, code=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Sonuncu ayda deyilsiniz"}, status=status.HTTP_400_BAD_REQUEST) 

        
        create_olunacaq_ay_price = last_month.price - odemek_istediyi_amount
        last_month.price = odemek_istediyi_amount
        # last_month.odenme_status = "ÖDƏNƏN"
        last_month.sertli_odeme_status = "SON AYIN BÖLÜNMƏSİ"
        last_month.note = note
        last_month.save()

        residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
        # muqavile.residue_borc = residue_borc
        muqavile.save()

        inc_month = pd.date_range(last_month.date, periods = 2, freq='M')
        Installment.objects.create(
            month_no = int(last_month.month_no) + 1,
            muqavile = muqavile,
            date = f"{inc_month[1].year}-{inc_month[1].month}-{last_month.date.day}",
            price = create_olunacaq_ay_price
        ).save()
        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    # Odenen ay ile bagli emeliyyat
    if((now_ay.odenme_status == "ÖDƏNMƏYƏN" and float(odemek_istediyi_amount) == now_ay.price)):
        odenmeyen_odemedateler_qs = Installment.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemedateler = list(odenmeyen_odemedateler_qs)
        if serializer.is_valid():
            now_ay.odenme_status = "ÖDƏNƏN"
            # now_ay.note = note
            now_ay.save()
            if(now_ay == odenmeyen_odemedateler[-1]):
                muqavile.muqavile_status = "BİTMİŞ"
                muqavile.save()
            
            residue_borc = float(residue_borc) - float(odemek_istediyi_amount)
            muqavile.residue_borc = residue_borc
            muqavile.save()

            ilkin_balance = holding_umumi_balance_hesabla()
            print(f"{ilkin_balance=}")
            ofis_ilkin_balance = ofis_balance_hesabla(ofis=ofis)
            
            note = f"Vanleader - {responsible_employee_1.asa}, müştəri - {musteri.asa}, date - {today}, ödəniş üslubu - {payment_style}. kredit ödəməsi"
            c_income(ofis_cashbox, float(odemek_istediyi_amount), responsible_employee_1, note)

            sonraki_balance = holding_umumi_balance_hesabla()
            print(f"{sonraki_balance=}")
            ofis_sonraki_balance = ofis_balance_hesabla(ofis=ofis)
            pul_axini_create(
                ofis=ofis,
                shirket=ofis.shirket,
                aciqlama=note,
                ilkin_balance=ilkin_balance,
                sonraki_balance=sonraki_balance,
                ofis_ilkin_balance=ofis_ilkin_balance,
                ofis_sonraki_balance=ofis_sonraki_balance,
                emeliyyat_eden=user,
                emeliyyat_uslubu="MƏDAXİL",
                miqdar=float(odemek_istediyi_amount)
            )

            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            traceback.print_exc()
            return Response({"detail": "Xəta"}, status=status.HTTP_400_BAD_REQUEST)
            # return ValidationError(detail={"detail": "Məlumatları doğru daxil edin"}, code=status.HTTP_400_BAD_REQUEST)
            
    else:
        traceback.print_exc()
        return Response({"detail": "Yanlış əməliyyat"}, status=status.HTTP_400_BAD_REQUEST)
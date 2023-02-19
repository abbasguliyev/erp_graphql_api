from rest_framework import status

from rest_framework.response import Response
from cashbox.models import OfficeCashbox

from warehouse.models import (
    Anbar,
    Stok
)

from restAPI.v1.contract.utils.muqavile_utils import (
    reduce_product_from_stock, 
    add_product_to_stock, 
    c_income, 
    expense
)
from rest_framework.generics import get_object_or_404


def muqavile_hediyye_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        mehsullar = serializer.validated_data.get("mehsul")
        muqavile = serializer.validated_data.get("muqavile")
        responsible_employee_1 = muqavile.responsible_employee_1
        quantity = serializer.validated_data.get("quantity")
        if quantity == None or quantity == "":
            quantity = 1

        if muqavile.ofis == None:
            ofis = serializer.validated_data.get("ofis")
            if ofis == None or ofis == "":
                return Response({"detail": "Office daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ofis = muqavile.ofis

        try:
            anbar = get_object_or_404(Anbar, ofis=ofis)
        except:
            return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

        for mehsul in mehsullar:
            try:
                stock = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
                reduce_product_from_stock(stock, quantity)
            except:
                return Response({"detail": "Stokda məhsul qalmayıb"}, status=status.HTTP_404_NOT_FOUND)

            if mehsul.price > 0:
                try:
                    cashbox = OfficeCashbox.objects.filter(ofis=ofis)[0]
                except:
                    return Response({"detail": "Office Cashbox tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
                the_amount_to_enter = float(mehsul.price)*int(quantity)
                note = f"{muqavile} müqviləsinə {user.asa} tərəfindən {quantity} ədəd {mehsul} hədiyyə verildiyi üçün, {cashbox} ofis cashboxsına {the_amount_to_enter} AZN mədaxil edildi"
                c_income(
                    company_cashbox=cashbox,
                    the_amount_to_enter=the_amount_to_enter,
                    responsible_employee_1=user,
                    note=note
                )

        serializer.save(ofis=ofis)
        return Response({"detail": f"Müştəri {muqavile.musteri.asa} ilə müqaviləyə hədiyyə təyin olundu."}, status=status.HTTP_200_OK)


def muqavile_hediyye_destroy(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    muqavile_hediyye = self.get_object()
    user = request.user

    mehsul_query_set = muqavile_hediyye.mehsul.all()
    mehsullar = list(mehsul_query_set)
    muqavile = muqavile_hediyye.muqavile
    responsible_employee_1 = muqavile.responsible_employee_1
    anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
    quantity = muqavile_hediyye.quantity
    for mehsul in mehsullar:
        ofis = muqavile.ofis
        if mehsul.price > 0:
            try:
                cashbox = OfficeCashbox.objects.filter(ofis=ofis)[0]
            except:
                return Response({"detail": "Office Cashbox tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
            the_amount_to_enter = float(mehsul.price)*int(quantity)
            if the_amount_to_enter > float(cashbox.balance):
                return Response({"detail": "Cashboxnın balanceında yetəri qədər məbləğ yoxdur"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                note = f"{muqavile} müqviləsindən {user.asa} tərəfindən {quantity} ədəd {mehsul} hədiyyəsi geri alındığı üçün, {cashbox} ofis cashboxsından {the_amount_to_enter} AZN məxaric edildi"
                expense(
                    company_cashbox=cashbox,
                    the_amount_to_enter=the_amount_to_enter,
                    responsible_employee_1=user,
                    note=note
                )
        try:
            stock = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            add_product_to_stock(stock, quantity)
        except:
            stock = Stok.objects.create(anbar=anbar, mehsul=mehsul, quantity=quantity)
            stock.save()
        
    muqavile_hediyye.delete()
    return Response({"detail": "Hədiyyə stock-a geri qaytarıldı"}, status=status.HTTP_200_OK)

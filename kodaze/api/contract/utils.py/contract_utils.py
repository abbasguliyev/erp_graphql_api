import math
from account.models import User, Customer
from company.models import Office, Department, Position
from cashbox.models import OfficeCashbox
from income_expense.models import OfficeCashboxIncome, OfficeCashboxExpense
from salary.models import (
    DealerPrimNew,
    SalaryView,
    OfficeLeaderPrim,
    VanLeaderPrimNew
)
from contract.models import Installment
from warehouse.models import (
    Warehouse,
    Stock
)
from product.models import Product
from services.models import Service, ServicePayment
import pandas as pd
import datetime
import traceback
from services.signals import create_services

from core.utils.ocean_contract_pdf_create import (
    ocean_contract_pdf_canvas,
    ocean_create_contract_pdf,
    ocean_installment_contract_pdf_canvas,
    ocean_installment_create_contract_pdf,
)

from core.utils.magnus_contract_pdf_create import (
    magnus_create_contract_pdf,
    magnus_contract_pdf_canvas,
    magnus_installment_create_contract_pdf,
    magnus_installment_contract_pdf_canvas,
)

from api.cashbox.utils import (
    calculate_holding_total_balance,
    create_cash_flow,
    calculate_office_balance,
)


def create_and_add_pdf_when_contract_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = ocean_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = magnus_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf = contract_pdf
        instance.save()


def create_and_add_pdf_when_contract_installment_updated(sender, instance, created, **kwargs):
    if created:
        print("create_and_add_pdf_when_contract_installment_updated işə düşdü")

        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = ocean_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = magnus_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf_elave = contract_pdf
        instance.save()


def pdf_create_when_contract_updated(sender, instance, created):
    create_and_add_pdf_when_contract_updated(
        sender=sender, instance=instance, created=created)
    create_and_add_pdf_when_contract_installment_updated(
        sender=sender, instance=instance, created=created)
# ----------------------------------------------------------------------------------------------------------------------


def reduce_product_from_stock(stock, product_quantity):
    stock.quantity = stock.quantity - int(product_quantity)
    stock.save()
    if (stock.quantity == 0):
        stock.delete()
    return stock.quantity


def add_product_to_stock(stock, product_quantity):
    stock.quantity = stock.quantity + int(product_quantity)
    stock.save()
    return stock.quantity


def c_income(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(the_amount_to_enter) + float(company_cashbox.balance)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    income = OfficeCashboxIncome.objects.create(
        executor=responsible_employee_1,
        office_cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    income.save()
    return income


def expense(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(company_cashbox.balance) - float(the_amount_to_enter)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    expense = OfficeCashboxExpense.objects.create(
        executor=responsible_employee_1,
        office_cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    expense.save()
    return expense

# ----------------------------------------------------------------------------------------------------------------------


def create_installment_when_update_contract(
    instance, loan_term, payment_style, initial_payment, initial_payment_debt,  **kwargs
):
    """
    Bu method ne zaman contract negd odenisden installmente kecirilerse o zaman ishe dushur.
    """

    loan_term = loan_term
    product_quantity = instance.product_quantity

    def loan_term_func(loan_term, product_quantity):
        new_loan_term = loan_term * product_quantity
        return new_loan_term

    if(payment_style == "KREDİT"):

        now = datetime.datetime.today().strftime('%d-%m-%Y')
        inc_month = pd.date_range(now, periods=loan_term+1, freq='M')

        initial_payment = initial_payment
        initial_payment_debt = initial_payment_debt

        if(initial_payment is not None):
            initial_payment = float(initial_payment)

        if(initial_payment_debt is not None):
            initial_payment_debt = float(initial_payment_debt)

        total_amount = instance.total_amount

        if(initial_payment_debt == 0):
            initial_payment_full = initial_payment
        elif(initial_payment_debt != 0):
            initial_payment_full = initial_payment + initial_payment_debt

        total_amount_to_be_paid_for_the_month = total_amount - initial_payment_full

        if(loan_term > 0):
            amount_to_be_paid_by_month = total_amount_to_be_paid_for_the_month // loan_term

            residue = amount_to_be_paid_by_month * (loan_term - 1)
            amount_to_be_paid_in_the_last_month = total_amount_to_be_paid_for_the_month - residue

            i = 1
            while(i <= loan_term):
                if(i == loan_term):
                    if(datetime.date.today().day < 29):
                        Installment.objects.create(
                            month_no=i,
                            contract=instance,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            price=amount_to_be_paid_in_the_last_month
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                price=amount_to_be_paid_in_the_last_month
                            ).save()
                        else:
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                price=amount_to_be_paid_in_the_last_month,
                                last_month=True
                            ).save()
                else:
                    if(datetime.date.today().day < 29):
                        Installment.objects.create(
                            month_no=i,
                            contract=instance,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            price=amount_to_be_paid_by_month
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                price=amount_to_be_paid_by_month
                            ).save()
                        else:
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                price=amount_to_be_paid_by_month
                            ).save()
                i += 1


def contract_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = None

    responsible_employee_1_id = request.data.get("responsible_employee_1_id")

    if (responsible_employee_1_id == None):
        user = self.request.user
    else:
        user = get_object_or_404(User, pk=responsible_employee_1_id)

    dealer_id = request.data.get("dealer_id")
    canvesser_id = request.data.get("canvesser_id")

    customer_id = request.data.get("customer_id")
    if customer_id == None:
        return Response({"detail": "Müştəri note olunmayıb"}, status=status.HTTP_400_BAD_REQUEST)
    customer = get_object_or_404(Musteri, pk=customer_id)

    dealer = None
    canvesser = None

    if (dealer_id is not None):
        try:
            dealer = get_object_or_404(User, pk=dealer_id)
            if (canvesser_id == None):
                canvesser = dealer
        except:
            return Response({"detail": "Dealer tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    if (canvesser_id is not None):
        try:
            canvesser = get_object_or_404(User, pk=canvesser_id)
            if (dealer_id == None):
                dealer = canvesser
        except:
            return Response({"detail": "Canvesser tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    my_time = datetime.datetime.min.time()

    now_date_date = datetime.date.today()
    now_date = datetime.datetime.combine(now_date_date, my_time)
    now_date_san = datetime.datetime.timestamp(now_date)

    if (request.data.get("initial_payment_date") is not None):
        initial_payment_date = request.data.get("initial_payment_date")
        initial_payment_date_date = datetime.datetime.strptime(
            initial_payment_date, "%d-%m-%Y")
        initial_payment_date_san = datetime.datetime.timestamp(
            initial_payment_date_date)
    # else:
    #     initial_payment_date = now_date_date
    #     initial_payment_date_date = now_date
    #     initial_payment_date_san = now_date_san

    # if (request.data.get("contract_date") is not None):
    #     contract_date = request.data.get("contract_date")
    # else:
    #     contract_date = datetime.date.today()

    if (request.data.get("initial_payment_debt_date") is not None):
        initial_payment_debt_date = request.data.get(
            "initial_payment_debt_date")
        initial_payment_debt_date_date = datetime.datetime.strptime(
            initial_payment_debt_date, "%d-%m-%Y")
        initial_payment_debt_date_san = datetime.datetime.timestamp(
            initial_payment_debt_date_date)

    if (request.data.get("negd_odenis_1_date") is not None):
        negd_odenis_1_date = request.data.get("negd_odenis_1_date")
        negd_odenis_1_date_date = datetime.datetime.strptime(
            negd_odenis_1_date, "%d-%m-%Y")
        negd_odenis_1_date_san = datetime.datetime.timestamp(
            negd_odenis_1_date_date)

    if (request.data.get("negd_odenis_2_date") is not None):
        negd_odenis_2_date = request.data.get("negd_odenis_2_date")
        negd_odenis_2_date_date = datetime.datetime.strptime(
            negd_odenis_2_date, "%d-%m-%Y")
        negd_odenis_2_date_san = datetime.datetime.timestamp(
            negd_odenis_2_date_date)

    mehsul_id_str = request.data.get("mehsul_id")
    if (mehsul_id_str == None):
        return Response({"detail": "Müqavilə imzalamaq üçün mütləq məhsul daxil edilməlidir."},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        mehsul_id = int(mehsul_id_str)

    try:
        mehsul = get_object_or_404(Mehsullar, pk=mehsul_id)
    except:
        return Response({"detail": "Məhsul tapılmadı"},
                        status=status.HTTP_400_BAD_REQUEST)

    product_quantity = request.data.get("product_quantity")
    if (product_quantity == None):
        product_quantity = 1

    payment_style = request.data.get("payment_style")

    initial_payment = request.data.get("initial_payment")

    initial_payment_debt = request.data.get("initial_payment_debt")

    def umumi_amount(mehsul_pricei, product_quantity):
        total_amount = mehsul_pricei * product_quantity
        return total_amount

    if (product_quantity == None):
        product_quantity = 1

    total_amount = umumi_amount(mehsul.price, int(product_quantity))

    office_id = request.data.get("office_id")

    company_id = request.data.get("company_id")

    shobe_id = request.data.get("shobe_id")

    loan_term = request.data.get("loan_term")

    if (user.office == None):
        office = Office.objects.get(pk=office_id)
    else:
        office = user.office
    if (user.company == None):
        company = mehsul.company
    else:
        company = user.company

    if (shobe_id is not None):
        shobe = Shobe.objects.get(pk=shobe_id)
    else:
        shobe = user.shobe
    try:
        anbar = get_object_or_404(Anbar, office=office)
    except:
        traceback.print_exc()
        return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        office_cashbox = get_object_or_404(OfficeCashbox, office=office)
    except:
        traceback.print_exc()
        return Response({"detail": "Office Cashbox tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    office_cashbox_balance = office_cashbox.balance
    residue_borc = 0

    try:
        try:
            stock = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
        except:
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        if (stock.quantity < int(product_quantity)):
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if (serializer.is_valid()):
            if (product_quantity == None):
                product_quantity = 1
            # Kredit
            if (payment_style == "KREDİT"):
                if (loan_term == None):
                    # Kredit muddeti daxil edilmezse
                    return Response({"detail": "Ödəmə statusu installmentdir amma installment müddəti daxil edilməyib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) == 0):
                    # Kredit muddeyi 0 daxil edilerse
                    return Response({"detail": "Ödəmə statusu installmentdir amma installment müddəti 0 daxil edilib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 30):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum installment müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 0):
                    # Kredit muddeti 0-dan boyuk olarsa

                    if ((initial_payment is not None) and (request.data.get("initial_payment_date") == None)):
                        initial_payment_date = now_date_date
                        initial_payment_date_date = now_date
                        initial_payment_date_san = now_date_san

                    if ((initial_payment_debt is not None) and (request.data.get("initial_payment_debt_date") == None)):
                        return Response({
                            "detail": "Qalıq İlkin ödəniş məbləği note olunub amma qalıq ilkin ödəniş date note olunmayıb"},
                            status=status.HTTP_400_BAD_REQUEST)

                    if (initial_payment == None and initial_payment_debt == None):
                        # Ilkin odenis daxil edilmezse
                        reduce_product_from_stock(stock, int(product_quantity))
                        total_amount = umumi_amount(
                            mehsul.price, int(product_quantity))

                        residue_borc = float(total_amount)

                        serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company, office=office,
                                        shobe=shobe, total_amount=total_amount, residue_borc=residue_borc)
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    elif (initial_payment is not None and initial_payment_debt == None):
                        total_amount = umumi_amount(
                            mehsul.price, int(product_quantity))
                        if float(initial_payment) >= float(total_amount):
                            return Response({"detail": "İlkin ödəniş məbləği müqavilənin məbləğindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        # Umumi ilkin odenis amounti daxil edilerse ve residue ilkin odenis amounti daxil edilmezse
                        if (now_date_san == initial_payment_date_san):
                            print(f"*****************{initial_payment_date=}")
                            reduce_product_from_stock(stock, int(product_quantity))
                            total_amount = umumi_amount(
                                mehsul.price, int(product_quantity))

                            ilkin_balance = calculate_holding_total_balance()
                            print(f"{ilkin_balance=}")
                            office_ilkin_balance = calculate_office_balance(
                                office=office)
                            note = f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş"
                            c_income(office_cashbox, float(
                                initial_payment), user, note)

                            residue_borc = float(
                                total_amount) - float(initial_payment)
                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, initial_payment=initial_payment,
                                            initial_payment_status="BİTMİŞ", total_amount=total_amount, residue_borc=residue_borc,)
                            sonraki_balance = calculate_holding_total_balance()
                            print(f"{sonraki_balance=}")
                            office_sonraki_balance = calculate_office_balance(
                                office=office)
                            create_cash_flow(
                                office=office,
                                company=office.company,
                                aciqlama=f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş",
                                ilkin_balance=ilkin_balance,
                                sonraki_balance=sonraki_balance,
                                office_ilkin_balance=office_ilkin_balance,
                                office_sonraki_balance=office_sonraki_balance,
                                emeliyyat_eden=user,
                                emeliyyat_uslubu="MƏDAXİL",
                                miqdar=float(initial_payment)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (now_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stock, int(product_quantity))
                            total_amount = umumi_amount(
                                mehsul.price, int(product_quantity))

                            residue_borc = float(
                                total_amount) - float(initial_payment)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, initial_payment=initial_payment,
                                            initial_payment_status="DAVAM EDƏN", residue_borc=residue_borc,
                                            total_amount=total_amount)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (now_date_san > initial_payment_date_san):
                            return Response({"detail": "İlkin ödəniş dateni keçmiş dateə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)

                    elif ((initial_payment == None and initial_payment_debt is not None) or (
                            float(initial_payment) == 0 and initial_payment_debt is not None)):
                        return Response({"detail": "İlkin ödəniş daxil edilmədən qalıq ilkin ödəniş daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (float(initial_payment) == 0):
                        # Umumi ilkin odenis amounti 0 olarsa
                        return Response({"detail": "İlkin ödəniş 0 azn daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif (initial_payment_debt is not None):
                        total_amount2 = umumi_amount(
                            mehsul.price, int(product_quantity))
                        residue_borc2 = float(
                            total_amount2) - float(initial_payment_debt)
                        if float(initial_payment) >= float(residue_borc2):
                            return Response({"detail": "İlkin ödəniş qalıq məbləği qalıq məbləğdən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        if ((now_date_san == initial_payment_date_san) and (
                                now_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stock, int(product_quantity))
                            total_amount = umumi_amount(
                                mehsul.price, int(product_quantity))

                            ilkin_balance = calculate_holding_total_balance()
                            print(f"{ilkin_balance=}")
                            office_ilkin_balance = calculate_office_balance(
                                office=office)

                            note = f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi."
                            c_income(office_cashbox, float(
                                initial_payment), user, note)

                            residue_borc = float(
                                total_amount) - float(initial_payment)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="BİTMİŞ",
                                            residue_initial_payment_status="DAVAM EDƏN",
                                            total_amount=total_amount, residue_borc=residue_borc)
                            sonraki_balance = calculate_holding_total_balance()
                            print(f"{sonraki_balance=}")
                            office_sonraki_balance = calculate_office_balance(
                                office=office)
                            create_cash_flow(
                                office=office,
                                company=office.company,
                                aciqlama=f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi.",
                                ilkin_balance=ilkin_balance,
                                sonraki_balance=sonraki_balance,
                                office_ilkin_balance=office_ilkin_balance,
                                office_sonraki_balance=office_sonraki_balance,
                                emeliyyat_eden=user,
                                emeliyyat_uslubu="MƏDAXİL",
                                miqdar=float(initial_payment)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        elif ((now_date_san == initial_payment_date_san) and (
                                initial_payment_date_san == initial_payment_debt_date_san)):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi bu günki dateə note oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (now_date_san == initial_payment_debt_date_san):
                            return Response({"detail": "İlkin ödəniş qalıq bu günki dateə note oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san > initial_payment_debt_date_san):
                            return Response(
                                {"detail": "İlkin ödəniş qalıq date ilkin ödəniş datendən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san == initial_payment_debt_date_san):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi eyni dateə note oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif ((now_date_san > initial_payment_date_san) or (
                                now_date_san > initial_payment_debt_date_san)):
                            return Response({"detail": "İlkin ödəniş dateni keçmiş dateə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (now_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stock, int(product_quantity))
                            total_amount = umumi_amount(
                                mehsul.price, int(product_quantity))

                            # residue_borc = float(total_amount) - float(initial_payment_debt) - float(initial_payment)
                            residue_borc = float(total_amount)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="DAVAM EDƏN",
                                            residue_initial_payment_status="DAVAM EDƏN",
                                            total_amount=total_amount, residue_borc=residue_borc)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif ((now_date_san < initial_payment_date_san) and (
                                now_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stock, int(product_quantity))
                            total_amount = umumi_amount(
                                mehsul.price, int(product_quantity))

                            # residue_borc = float(total_amount) - float(initial_payment_debt) - float(initial_payment)
                            residue_borc = float(total_amount)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="DAVAM EDƏN",
                                            residue_initial_payment_status="DAVAM EDƏN",
                                            total_amount=total_amount, residue_borc=residue_borc)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response({"detail": "Qalıq ilkin ödəniş doğru daxil edilməyib."},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Negd odenis
            elif (payment_style == "NƏĞD" and request.data.get("negd_odenis_1") == None and request.data.get("negd_odenis_2") == None):
                if (loan_term is not None):
                    return Response({"detail": "Kredit müddəti ancaq status installment olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (initial_payment is not None or initial_payment_debt is not None):
                    return Response({"detail": "İlkin ödəniş ancaq status installment olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (product_quantity == None):
                    product_quantity = 1

                reduce_product_from_stock(stock, int(product_quantity))
                total_amount = umumi_amount(
                    mehsul.price, int(product_quantity))

                ilkin_balance = calculate_holding_total_balance()
                print(f"{ilkin_balance=}")
                office_ilkin_balance = calculate_office_balance(office=office)

                note = f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {now_date_date}, ödəniş üslubu - {payment_style}"
                c_income(office_cashbox, float(
                    total_amount), user, note)

                serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company, office=office,
                                contract_status="BİTMİŞ", shobe=shobe, total_amount=total_amount)

                sonraki_balance = calculate_holding_total_balance()
                print(f"{sonraki_balance=}")
                office_sonraki_balance = calculate_office_balance(office=office)
                create_cash_flow(
                    office=office,
                    company=office.company,
                    aciqlama=note,
                    ilkin_balance=ilkin_balance,
                    sonraki_balance=sonraki_balance,
                    office_ilkin_balance=office_ilkin_balance,
                    office_sonraki_balance=office_sonraki_balance,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏDAXİL",
                    miqdar=float(total_amount)
                )
                # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"}, status=status.HTTP_201_CREATED)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            # 2 defeye negd odenis
            elif (request.data.get("negd_odenis_1") is not None and request.data.get("negd_odenis_2") is not None):
                if (float(request.data.get("negd_odenis_1")) < total_amount):
                    if (product_quantity == None):
                        product_quantity = 1
                    if (loan_term is not None):
                        return Response({"detail": "Kredit müddəti ancaq status installment olan müqavilələr üçündür"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    negd_odenis_1 = request.data.get("negd_odenis_1")
                    negd_odenis_2 = request.data.get("negd_odenis_2")
                    total_amount = umumi_amount(
                        mehsul.price, int(product_quantity))

                    if (negd_odenis_1 == None or negd_odenis_2 == None or negd_odenis_1 == "0" or negd_odenis_2 == "0"):
                        return Response(
                            {"detail": "2 dəfəyə nəğd ödəniş statusunda hər 2 nəğd ödəniş note olunmalıdır"},
                            status=status.HTTP_400_BAD_REQUEST)
                    elif float(negd_odenis_1) > total_amount or float(negd_odenis_2) > total_amount:
                        return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif float(negd_odenis_1) + float(negd_odenis_2) == total_amount:
                        if ((now_date_san == negd_odenis_1_date_san) and (
                                now_date_san < negd_odenis_2_date_san)):
                            reduce_product_from_stock(stock, int(product_quantity))

                            ilkin_balance = calculate_holding_total_balance()
                            print(f"{ilkin_balance=}")
                            office_ilkin_balance = calculate_office_balance(
                                office=office)

                            note = f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {negd_odenis_1_date}, ödəniş üslubu - {payment_style}, 1-ci nəğd ödəniş"
                            c_income(office_cashbox, float(
                                negd_odenis_1), user, note)

                            residue_borc = float(
                                total_amount) - float(negd_odenis_1)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, payment_style="İKİ DƏFƏYƏ NƏĞD",
                                            negd_odenis_1_status="BİTMİŞ", negd_odenis_2_status="DAVAM EDƏN",
                                            total_amount=total_amount, residue_borc=residue_borc)
                            sonraki_balance = calculate_holding_total_balance()
                            print(f"{sonraki_balance=}")
                            office_sonraki_balance = calculate_office_balance(
                                office=office)
                            create_cash_flow(
                                office=office,
                                company=office.company,
                                aciqlama=note,
                                ilkin_balance=ilkin_balance,
                                sonraki_balance=sonraki_balance,
                                office_ilkin_balance=office_ilkin_balance,
                                office_sonraki_balance=office_sonraki_balance,
                                emeliyyat_eden=user,
                                emeliyyat_uslubu="MƏDAXİL",
                                miqdar=float(negd_odenis_1)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                        elif ((now_date_san == negd_odenis_1_date_san) and (
                                negd_odenis_1_date_san == negd_odenis_2_date_san)):
                            return Response({"detail": "Ödənişlərin hər ikisi bu günki dateə note oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (now_date_san == negd_odenis_2_date_san):
                            return Response({"detail": "Qalıq nəğd ödəniş bu günki dateə note oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (negd_odenis_1_date_san > negd_odenis_2_date_san):
                            return Response(
                                {"detail": "Qalıq nəğd ödəniş date nəğd ödəniş datendən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

                        elif (negd_odenis_1_date_san == negd_odenis_2_date_san):
                            return Response(
                                {"detail": "Qalıq nəğd ödəniş və nəğd ödəniş hər ikisi eyni dateə note oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

                        elif ((now_date_san > negd_odenis_1_date_san) or (
                                now_date_san > negd_odenis_2_date_san)):
                            return Response({"detail": "Nəğd ödəniş dateni keçmiş dateə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif ((now_date_san < negd_odenis_1_date_san) and (
                                now_date_san < negd_odenis_2_date_san)):
                            reduce_product_from_stock(stock, int(product_quantity))

                            residue_borc = float(total_amount)

                            serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company,
                                            office=office, shobe=shobe, payment_style="İKİ DƏFƏYƏ NƏĞD",
                                            negd_odenis_1_status="DAVAM EDƏN", negd_odenis_2_status="DAVAM EDƏN",
                                            total_amount=total_amount, residue_borc=residue_borc)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                    elif (float(negd_odenis_1) + float(negd_odenis_2) != total_amount):
                        return Response({"detail": "Ödəmək istədiyiniz məbləğlər məhsulun qiymətinə bərabər deyil"},
                                        status=status.HTTP_400_BAD_REQUEST)

            elif (request.data.get("negd_odenis_1") is not None and request.data.get("negd_odenis_2") == None):
                return Response({"detail": "Nəğd ödəniş 2 daxil edilməyib"}, status=status.HTTP_400_BAD_REQUEST)

            elif (payment_style == "İKİ DƏFƏYƏ NƏĞD"):
                if (product_quantity == None):
                    product_quantity = 1
                if (loan_term is not None):
                    return Response({"detail": "Kredit müddəti ancaq status installment olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)

                negd_odenis_1 = request.data.get("negd_odenis_1")
                negd_odenis_2 = request.data.get("negd_odenis_2")
                total_amount = umumi_amount(
                    mehsul.price, int(product_quantity))

                if (negd_odenis_1 == None or negd_odenis_2 == None or negd_odenis_1 == "0" or negd_odenis_2 == "0"):
                    return Response({"detail": "2 dəfəyə nəğd ödəniş statusunda hər 2 nəğd ödəniş note olunmalıdır"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (float(negd_odenis_1) > total_amount):
                    return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                    status=status.HTTP_400_BAD_REQUEST)

                elif (float(negd_odenis_2) > total_amount):
                    return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (float(negd_odenis_1) + float(negd_odenis_2) == total_amount):

                    if ((now_date_san == negd_odenis_1_date_san) and (now_date_san < negd_odenis_2_date_san)):
                        reduce_product_from_stock(stock, int(product_quantity))

                        ilkin_balance = calculate_holding_total_balance()
                        print(f"{ilkin_balance=}")
                        office_ilkin_balance = calculate_office_balance(
                            office=office)

                        note = f"Vanleader - {user.asa}, müştəri - {customer.asa}, date - {negd_odenis_1_date}, ödəniş üslubu - {payment_style}, 1-ci nəğd ödəniş"
                        c_income(office_cashbox, float(
                            negd_odenis_1), user, note)

                        residue_borc = float(
                            total_amount) - float(negd_odenis_1)

                        serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company, office=office,
                                        shobe=shobe, negd_odenis_1_status="BİTMİŞ", negd_odenis_2_status="DAVAM EDƏN",
                                        total_amount=total_amount, residue_borc=residue_borc)
                        sonraki_balance = calculate_holding_total_balance()
                        print(f"{sonraki_balance=}")
                        office_sonraki_balance = calculate_office_balance(
                            office=office)
                        create_cash_flow(
                            office=office,
                            company=office.company,
                            aciqlama=note,
                            ilkin_balance=ilkin_balance,
                            sonraki_balance=sonraki_balance,
                            office_ilkin_balance=office_ilkin_balance,
                            office_sonraki_balance=office_sonraki_balance,
                            emeliyyat_eden=user,
                            emeliyyat_uslubu="MƏDAXİL",
                            miqdar=float(negd_odenis_1)
                        )
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                    elif ((now_date_san == negd_odenis_1_date_san) and (
                            negd_odenis_1_date_san == negd_odenis_2_date_san)):
                        return Response({"detail": "Ödənişlərin hər ikisi bu günki dateə note oluna bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (now_date_san == negd_odenis_2_date_san):
                        return Response({"detail": "Qalıq nəğd ödəniş bu günki dateə note oluna bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (negd_odenis_1_date_san > negd_odenis_2_date_san):
                        return Response({"detail": "Qalıq nəğd ödəniş date nəğd ödəniş datendən əvvəl ola bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (negd_odenis_1_date_san == negd_odenis_2_date_san):
                        return Response(
                            {"detail": "Qalıq nəğd ödəniş və nəğd ödəniş hər ikisi eyni dateə note oluna bilməz"},
                            status=status.HTTP_400_BAD_REQUEST)

                    elif ((now_date_san > negd_odenis_1_date_san) or (now_date_san > negd_odenis_2_date_san)):
                        return Response({"detail": "Nəğd ödəniş dateni keçmiş dateə təyin edə bilməzsiniz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif ((now_date_san < negd_odenis_1_date_san) and (
                            now_date_san < negd_odenis_2_date_san)):
                        reduce_product_from_stock(stock, int(product_quantity))

                        residue_borc = float(total_amount)

                        serializer.save(responsible_employee_1=user, dealer=dealer, canvesser=canvesser, company=company, office=office,
                                        shobe=shobe, negd_odenis_1_status="DAVAM EDƏN",
                                        negd_odenis_2_status="DAVAM EDƏN", total_amount=total_amount, residue_borc=residue_borc)
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                elif (float(negd_odenis_1) + float(negd_odenis_2) != total_amount):
                    return Response({"detail": "Ödəmək istədiyiniz məbləğlər məhsulun qiymətinə bərabər deyil"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)


def contract_update(self, request, *args, **kwargs):
    try:
        contract = self.get_object()
        serializer = self.get_serializer(
            contract, data=request.data, partial=True)
        # serializer = MuqavileSerializer(contract, data=request.data, partial=True)
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        initial_payment_status = contract.initial_payment_status
        residue_initial_payment_status = contract.residue_initial_payment_status
        odemek_istediyi_initial_payment = request.data.get("initial_payment")
        odemek_istediyi_residue_initial_payment = request.data.get(
            "initial_payment_debt")

        negd_odenis_1 = contract.negd_odenis_1
        negd_odenis_2 = contract.negd_odenis_2
        negd_odenis_1_status = contract.negd_odenis_1_status
        negd_odenis_2_status = contract.negd_odenis_2_status

        contract_status = contract.contract_status
        odemek_istediyi_negd_odenis_1 = request.data.get("negd_odenis_1")
        odemek_istediyi_negd_odenis_2 = request.data.get("negd_odenis_2")
        my_time = datetime.datetime.min.time()

        now_date_date = datetime.date.today()
        now_date = datetime.datetime.combine(now_date_date, my_time)
        now_date_san = datetime.datetime.timestamp(now_date)
        dusen_contract_status = request.data.get("contract_status")
        mehsul = contract.mehsul
        product_quantity = contract.product_quantity
        contract_responsible_employee_1 = contract.responsible_employee_1
        office = contract.office
        customer = contract.customer
        customer_id = request.data.get("customer_id")
        if (customer_id is not None):
            customer = get_object_or_404(Musteri, pk=customer_id)

        contract_dealer = contract.dealer
        yeni_qrafik = request.data.get("yeni_qrafik_status")
        # YENI QRAFIK ile bagli emeliyyatlar
        if(yeni_qrafik == "YENİ QRAFİK"):
            print(
                "------------------------------------------------------------------------------------")
            initial_payment = contract.initial_payment
            initial_payment_debt = contract.initial_payment_debt
            initial_payment_full = initial_payment + initial_payment_debt
            total_amount = contract.total_amount
            odenen_odemedateler = Installment.objects.filter(
                contract=contract, odenme_status="ÖDƏNƏN")

            odenmeyen_odemedateler = Installment.objects.filter(
                contract=contract, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)

            sertli_odeme = Installment.objects.filter(
                contract=contract, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status=None)

            odenmeyen_odemedate_amount = Installment.objects.filter(
                contract=contract, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)[0].price

            odemek_istediyi_amount = float(
                request.data.get("yeni_qrafik_amount"))

            if odemek_istediyi_amount < odenmeyen_odemedate_amount:
                odenen_amount = 0
                for i in odenen_odemedateler:
                    odenen_amount += float(i.price)

                sertli_odemeden_gelen_amount = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_amount += float(s.price)
                print(f"***************{sertli_odeme=}")
                print(f"***************{sertli_odemeden_gelen_amount=}")
                odediyi = float(odenen_amount) + initial_payment_full
                residue_borc = total_amount - odediyi
                cixilacaq_amount = residue_borc - sertli_odemeden_gelen_amount

                odenmeyen_aylar = len(odenmeyen_odemedateler)
                try:
                    elave_olunacaq_ay_residueli = cixilacaq_amount / odemek_istediyi_amount
                    # contract.yeni_qrafik_status = "YENİ QRAFİK"
                    contract.residue_borc = residue_borc
                    contract.save()
                except:
                    return Response({"detail": "Ödəmək istədiyiniz məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

                elave_olunacaq_ay = math.ceil(elave_olunacaq_ay_residueli)
                create_olunacaq_ay = elave_olunacaq_ay - \
                    len(odenmeyen_odemedateler)
                a = odemek_istediyi_amount * (elave_olunacaq_ay-1)
                son_aya_elave_edilecek_amount = cixilacaq_amount - a
                inc_month = pd.date_range(odenmeyen_odemedateler[len(
                    odenmeyen_odemedateler)-1].date, periods=create_olunacaq_ay+1, freq='M')

                print(f"|||||||||||||||||||{inc_month=}")
                contract.loan_term = contract.loan_term + create_olunacaq_ay
                contract.save()
                # Var olan aylarin priceini customernin istediyi price edir
                i = 0
                while(i < len(odenmeyen_odemedateler)):
                    odenmeyen_odemedateler[i].price = odemek_istediyi_amount
                    odenmeyen_odemedateler[i].save()
                    i += 1
                # Elave olunacaq aylari create edir
                o_t = Installment.objects.filter(contract=contract)
                c = int(list(o_t)[-1].month_no) + 1
                print(f"***************{c=}")
                print(f"***************{create_olunacaq_ay=}")
                print(
                    f"***************{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                j = 1
                while(j <= create_olunacaq_ay):
                    if(j == create_olunacaq_ay):
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=c,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=son_aya_elave_edilecek_amount,
                                last_month=True
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            print(f"**************{j=}")
                            print(
                                f"***testson1***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                            print(
                                f"***testson1***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            print("Burdayam3")
                            if(inc_month[j].day <= datetime.date.today().day):
                                print(
                                    f"***testson2***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                                print(
                                    f"***testson2***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                                print("Burdayam4")
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=son_aya_elave_edilecek_amount,
                                    last_month=True
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=son_aya_elave_edilecek_amount,
                                    last_month=True
                                ).save()
                    else:
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=c,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=odemek_istediyi_amount
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            print(f"**************{j=}")
                            print(
                                f"***test***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                            print(
                                f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            print("Burdayam1")

                            print(
                                f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            if(inc_month[j].day <= datetime.date.today().day):
                                print(f"**************{j=}")
                                print(
                                    f"***test***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                                print(
                                    f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                                print("Burdayam2")

                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=odemek_istediyi_amount
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=odemek_istediyi_amount
                                ).save()
                    c += 1
                    j += 1

                pdf_create_when_contract_updated(
                    sender=contract, instance=contract, created=True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Məbləğ cari məbləğdən artıq ola bilməz!"}, status=status.HTTP_400_BAD_REQUEST)
        if (contract.contract_status == "DÜŞƏN" and request.data.get("contract_status") == "DAVAM EDƏN"):
            """
            Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
            """
            contract.contract_status = "DAVAM EDƏN"
            contract.is_sokuntu = False
            contract.save()

            try:
                anbar = get_object_or_404(Anbar, office=contract.office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stock = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            except:
                return Response({"detail": "Anbarın stockunda məhsul yoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            if (stock.quantity < int(product_quantity)):
                return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            reduce_product_from_stock(stock, product_quantity)

            contract_date = contract.contract_date
            year = contract_date.year
            month = contract_date.month
            date = datetime.date(year=year, month=month, day=1)
            odenmeyen_odemedateler_qs = Installment.objects.filter(
                contract=contract, odenme_status="ÖDƏNMƏYƏN")
            odenmeyen_odemedateler = list(odenmeyen_odemedateler_qs)
            now = datetime.datetime.today().strftime('%d-%m-%Y')
            inc_month = pd.date_range(now, periods=len(
                odenmeyen_odemedateler), freq='M')
            i = 0
            while (i < len(odenmeyen_odemedateler)):
                if (datetime.date.today().day < 29):
                    odenmeyen_odemedateler[
                        i].date = f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}"
                    odenmeyen_odemedateler[i].save()
                elif (
                        datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                    odenmeyen_odemedateler[i].date = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                    odenmeyen_odemedateler[i].save()
                i += 1

            create_services(contract, contract, True)

            return Response({"detail": "Müqavilə düşən statusundan davam edən statusuna keçirildi"},
                            status=status.HTTP_200_OK)

        if (contract.contract_status == "DAVAM EDƏN" and request.data.get("contract_status") == "DÜŞƏN"):
            """
            Müqavilə düşən statusuna keçərkən bu hissə işə düşür
            """
            contract_date = contract.contract_date
            year = contract_date.year
            month = contract_date.month
            date = datetime.date(year=year, month=month, day=1)
            kompensasiya_income = request.data.get("kompensasiya_income")
            kompensasiya_expense = request.data.get("kompensasiya_expense")

            contract_responsible_employee_1 = contract.responsible_employee_1
            contract_dealer = contract.dealer

            office_cashbox = get_object_or_404(OfficeCashbox, office=contract.office)
            office_cashbox_balance = office_cashbox.balance
            if (kompensasiya_income is not None and kompensasiya_expense is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (kompensasiya_income is not None):
                ilkin_balance = calculate_holding_total_balance()
                print(f"{ilkin_balance=}")
                office_ilkin_balance = calculate_office_balance(office=office)

                user = request.user
                customer = contract.customer

                note = f"Vanleader - {contract_responsible_employee_1.asa}, müştəri - {customer.asa}, date - {now_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_income}"
                c_income(office_cashbox, float(kompensasiya_income),
                          contract_responsible_employee_1, note)

                contract.contract_status = "DÜŞƏN"
                contract.kompensasiya_income = request.data.get(
                    "kompensasiya_income")
                contract.save()

                sonraki_balance = calculate_holding_total_balance()
                print(f"{sonraki_balance=}")
                office_sonraki_balance = calculate_office_balance(office=office)
                create_cash_flow(
                    office=contract.office,
                    company=contract.office.company,
                    aciqlama=note,
                    ilkin_balance=ilkin_balance,
                    sonraki_balance=sonraki_balance,
                    office_ilkin_balance=office_ilkin_balance,
                    office_sonraki_balance=office_sonraki_balance,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏDAXİL",
                    miqdar=float(kompensasiya_income)
                )

            elif (kompensasiya_expense is not None):
                if (office_cashbox_balance < float(kompensasiya_expense)):
                    return Response({"detail": "Kompensasiya məxaric məbləği Officein balanceından çox ola bilməz"},
                                    status=status.HTTP_400_BAD_REQUEST)
                ilkin_balance = calculate_holding_total_balance()
                print(f"{ilkin_balance=}")
                office_ilkin_balance = calculate_office_balance(office=office)

                user = request.user
                customer = contract.customer

                note = f"Vanleader - {contract_responsible_employee_1.asa}, müştəri - {customer.asa}, date - {now_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_expense}"
                expense(office_cashbox, float(kompensasiya_expense),
                          contract_responsible_employee_1, note)

                contract.contract_status = "DÜŞƏN"
                contract.kompensasiya_expense = request.data.get(
                    "kompensasiya_expense")
                contract.save()

                sonraki_balance = calculate_holding_total_balance()
                print(f"{sonraki_balance=}")
                office_sonraki_balance = calculate_office_balance(office=office)
                create_cash_flow(
                    office=contract.office,
                    company=contract.office.company,
                    aciqlama=note,
                    ilkin_balance=ilkin_balance,
                    sonraki_balance=sonraki_balance,
                    office_ilkin_balance=office_ilkin_balance,
                    office_sonraki_balance=office_sonraki_balance,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(kompensasiya_expense)
                )

            if (kompensasiya_income == "" and kompensasiya_expense == ""):
                contract.contract_status = "DÜŞƏN"
                contract.save()

            contract_responsible_employee_1 = contract.responsible_employee_1
            contract_dealer = contract.dealer

            try:
                anbar = get_object_or_404(Anbar, office=contract.office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            stock = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            add_product_to_stock(stock, product_quantity)

            now = datetime.date.today()
            d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
            next_m = d + pd.offsets.MonthBegin(1)

            all_servis = Servis.objects.filter(contract=contract)
            print(f"{all_servis=}")
            for servis in all_servis:
                all_servis_odeme = ServisOdeme.objects.filter(
                    servis=servis, odendi=False)
                print(f"{all_servis_odeme=}")
                if len(all_servis_odeme) == 1:
                    all_servis_odeme[0].delete()
                else:
                    for servis_odeme in all_servis_odeme:
                        print(f"{servis_odeme=}")
                        servis_odeme.delete()
                servis.delete()

            # -------------------- Maaslarin geri qaytarilmasi --------------------
            contract_payment_style = contract.payment_style
            responsible_employee_1 = contract.responsible_employee_1
            contract_loan_term = contract.loan_term

            try:
                vezife_adi = responsible_employee_1.vezife.vezife_adi
            except:
                vezife_adi = None

            if vezife_adi == "VANLEADER":
                if responsible_employee_1 is not None:
                    responsible_employee_1_status = responsible_employee_1.isci_status
                    try:
                        responsible_employee_1_vezife = responsible_employee_1.vezife.vezife_adi
                    except:
                        responsible_employee_1_vezife = None
                    if (responsible_employee_1_status is not None):
                        responsible_employee_1_prim = VanLeaderPrimNew.objects.get(
                            prim_status=responsible_employee_1_status, vezife=responsible_employee_1.vezife)
                        responsible_employee_1_mg_now_ay = SalaryView.objects.get(
                            isci=contract_responsible_employee_1, date=f"{now.year}-{now.month}-{1}")
                        responsible_employee_1_mg_novbeti_ay = SalaryView.objects.get(
                            isci=contract_responsible_employee_1, date=next_m)

                        responsible_employee_1_mg_now_ay.satis_quantityi = float(
                            responsible_employee_1_mg_now_ay.satis_quantityi) - float(product_quantity)
                        responsible_employee_1_mg_now_ay.satis_amounti = float(
                            responsible_employee_1_mg_now_ay.satis_amounti) - (float(contract.mehsul.price) * float(contract.product_quantity))

                        # responsible_employee_1_mg_novbeti_ay.yekun_maas = float(responsible_employee_1_mg_novbeti_ay.yekun_maas) - float(responsible_employee_1_prim.komandaya_gore_prim)

                        if contract_payment_style == "NƏĞD":
                            responsible_employee_1_mg_novbeti_ay.yekun_maas = float(
                                responsible_employee_1_mg_novbeti_ay.yekun_maas) - (float(responsible_employee_1_prim.negd) * float(contract.product_quantity))
                        elif contract_payment_style == "KREDİT":
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                responsible_employee_1_mg_novbeti_ay.yekun_maas = float(
                                    responsible_employee_1_mg_novbeti_ay.yekun_maas) - (float(responsible_employee_1_prim.negd) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                responsible_employee_1_mg_novbeti_ay.yekun_maas = float(responsible_employee_1_mg_novbeti_ay.yekun_maas) - (
                                    float(responsible_employee_1_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                responsible_employee_1_mg_novbeti_ay.yekun_maas = float(responsible_employee_1_mg_novbeti_ay.yekun_maas) - (
                                    float(responsible_employee_1_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                responsible_employee_1_mg_novbeti_ay.yekun_maas = float(responsible_employee_1_mg_novbeti_ay.yekun_maas) - (
                                    float(responsible_employee_1_prim.installment_19_24) * float(contract.product_quantity))

                        responsible_employee_1_mg_now_ay.save()
                        responsible_employee_1_mg_novbeti_ay.save()

                dealer = contract.dealer
                if dealer is not None:
                    dealer_status = dealer.isci_status
                    try:
                        dealer_vezife = dealer.vezife.vezife_adi
                    except:
                        dealer_vezife = None
                    if (dealer_vezife == "DEALER"):
                        dealer_prim = DealerPrimNew.objects.get(
                            prim_status=dealer_status, vezife=dealer.vezife)
                        dealer_mg_now_ay = SalaryView.objects.get(
                            isci=contract_dealer, date=f"{now.year}-{now.month}-{1}")
                        dealer_mg_novbeti_ay = SalaryView.objects.get(
                            isci=contract_dealer, date=next_m)

                        dealer_mg_now_ay.satis_quantityi = float(
                            dealer_mg_now_ay.satis_quantityi) - float(product_quantity)
                        dealer_mg_now_ay.satis_amounti = float(dealer_mg_now_ay.satis_amounti) - (
                            float(contract.mehsul.price) * float(contract.product_quantity))

                        if contract_payment_style == "NƏĞD":
                            dealer_mg_novbeti_ay.yekun_maas = float(
                                dealer_mg_novbeti_ay.yekun_maas) - (float(dealer_prim.negd) * float(contract.product_quantity))
                        elif contract_payment_style == "KREDİT":
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                dealer_mg_novbeti_ay.yekun_maas = float(
                                    dealer_mg_novbeti_ay.yekun_maas) - (float(dealer_prim.negd) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.installment_19_24) * float(contract.product_quantity))

                        dealer_mg_now_ay.save()
                        dealer_mg_novbeti_ay.save()

                office = contract.office
                if office is not None:
                    officeLeaderVezife = Vezifeler.objects.get(
                        vezife_adi="OFFICE LEADER", company=contract.company)
                    officeLeaders = User.objects.filter(
                        office=office, vezife=officeLeaderVezife)
                    for officeLeader in officeLeaders:
                        officeLeader_status = officeLeader.isci_status
                        officeleader_prim = OfficeLeaderPrim.objects.get(
                            prim_status=officeLeader_status, vezife=officeLeader.vezife)

                        officeLeader_maas_goruntulenme_bu_ay = SalaryView.objects.get(
                            isci=officeLeader, date=f"{now.year}-{now.month}-{1}")
                        officeLeader_maas_goruntulenme_novbeti_ay = SalaryView.objects.get(
                            isci=officeLeader, date=next_m)

                        officeLeader_maas_goruntulenme_bu_ay.satis_quantityi = float(
                            officeLeader_maas_goruntulenme_bu_ay.satis_quantityi) - float(product_quantity)
                        officeLeader_maas_goruntulenme_bu_ay.satis_amounti = float(
                            officeLeader_maas_goruntulenme_bu_ay.satis_amounti) - (float(contract.mehsul.price) * float(contract.product_quantity))
                        officeLeader_maas_goruntulenme_bu_ay.save()

                        officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas = float(
                            officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas) - (float(officeleader_prim.officee_gore_prim) * float(contract.product_quantity))
                        officeLeader_maas_goruntulenme_novbeti_ay.save()

            # -------------------- -------------------- --------------------
            contract.dusme_date = datetime.date.today()
            contract.contract_status = "DÜŞƏN"
            contract.is_sokuntu = True
            contract.save()

            return Response({"detail": "Müqavilə düşən statusuna keçirildi"}, status=status.HTTP_200_OK)

        if (contract.payment_style == "KREDİT"):
            if (odemek_istediyi_initial_payment != None and initial_payment_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_initial_payment) != initial_payment):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_initial_payment) == initial_payment):
                    contract.initial_payment_status = "BİTMİŞ"
                    contract.initial_payment_date = now_date_date
                    contract.residue_borc = float(
                        contract.residue_borc) - float(initial_payment)
                    contract.save()
                    return Response({"detail": "İlkin ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (odemek_istediyi_residue_initial_payment != None and initial_payment_status == "BİTMİŞ" and residue_initial_payment_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_residue_initial_payment) == initial_payment_debt):
                    contract.residue_initial_payment_status = "BİTMİŞ"
                    contract.initial_payment_debt_date = now_date_date
                    contract.residue_borc = float(
                        contract.residue_borc) - float(initial_payment_debt)
                    contract.save()
                    return Response({"detail": "Qalıq ilkin ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_residue_initial_payment) != initial_payment_debt):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        if (contract.payment_style == "İKİ DƏFƏYƏ NƏĞD"):
            if (odemek_istediyi_negd_odenis_1 != None and negd_odenis_1_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_1) != negd_odenis_1):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_negd_odenis_1) == negd_odenis_1):
                    contract.negd_odenis_1_status = "BİTMİŞ"
                    contract.negd_odenis_1_date = now_date_date
                    contract.residue_borc = float(
                        contract.residue_borc) - float(negd_odenis_1)
                    contract.save()
                    return Response({"detail": "1-ci ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (
                    odemek_istediyi_negd_odenis_2 != None and negd_odenis_1_status == "BİTMİŞ" and negd_odenis_2_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_2) == negd_odenis_2):
                    contract.negd_odenis_2_status = "BİTMİŞ"
                    contract.negd_odenis_2_date = now_date_date
                    contract.contract_status = "BİTMİŞ"
                    contract.residue_borc = float(
                        contract.residue_borc) - float(negd_odenis_2)
                    contract.save()
                    return Response({"detail": "Qalıq nəğd ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_negd_odenis_2) != negd_odenis_2):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        if contract.payment_style == "İKİ DƏFƏYƏ NƏĞD":
            if serializer.is_valid():
                loan_term = serializer.validated_data.get(
                    "loan_term")
                payment_style = serializer.validated_data.get("payment_style")

                if payment_style == "KREDİT":

                    initial_payment = 0
                    initial_payment_debt = 0
                    negd_odenis_1 = contract.negd_odenis_1
                    negd_odenis_2 = contract.negd_odenis_2
                    negd_odenis_1_date = contract.negd_odenis_1_date
                    negd_odenis_2_date = contract.negd_odenis_2_date
                    negd_odenis_1_status = contract.negd_odenis_1_status
                    negd_odenis_2_status = contract.negd_odenis_2_status

                    if negd_odenis_1_date != datetime.date.today():
                        negd_odenis_1_status = "DAVAM EDƏN"
                    else:
                        negd_odenis_1_status = "YOXDUR"

                    if negd_odenis_2_date != datetime.date.today():
                        negd_odenis_2_status = "DAVAM EDƏN"
                    else:
                        negd_odenis_2_status = "YOXDUR"

                    create_installment_when_update_contract(
                        instance=contract,
                        loan_term=int(loan_term),
                        payment_style=payment_style,
                        initial_payment=float(negd_odenis_1),
                        initial_payment_debt=0
                    )
                    serializer.save(
                        contract_status="DAVAM EDƏN",
                        initial_payment=negd_odenis_1,
                        initial_payment_debt=0,
                        initial_payment_date=negd_odenis_1_date,
                        initial_payment_debt_date=None,
                        initial_payment_status=negd_odenis_1_status,
                        residue_initial_payment_status="YOXDUR",
                        negd_odenis_1=0,
                        negd_odenis_2=0,
                        negd_odenis_1_date=None,
                        negd_odenis_2_date=None,
                        negd_odenis_1_status="YOXDUR",
                        negd_odenis_2_status="YOXDUR"
                    )
                    pdf_create_when_contract_updated(
                        sender=contract, instance=contract, created=True)
                    return Response({"detail": "Müqavilə nəğd statusundan installment statusuna keçirildi"}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Bu əməliyyatı icra etmək mümkün olmadı"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

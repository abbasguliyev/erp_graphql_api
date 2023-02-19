import datetime
from cashbox.models import HoldingCashbox, OfficeCashbox, CashFlow, CompanyCashbox

def calculate_holding_total_balance():
    total_balance = 0

    holding_cashbox = HoldingCashbox.objects.all()
    holding_balance = 0
    for hk in holding_cashbox:
        holding_balance += float(hk.balance)

    company_cashbox = CompanyCashbox.objects.all()
    company_balance = 0
    for sk in company_cashbox:
        company_balance += float(sk.balance)

    office_cashbox = OfficeCashbox.objects.all()
    office_balance = 0
    for ok in office_cashbox:
        office_balance += float(ok.balance)

    total_balance = holding_balance + company_balance + office_balance
    return total_balance

def calculate_holding_balance():
    holding_balance = 0
    holding_cashbox = HoldingCashbox.objects.all()[0]
    holding_balance += float(holding_cashbox.balance)
    return holding_balance

def calculate_company_balance(company):
    company_balance = 0
    company_cashbox = CompanyCashbox.objects.get(company=company)
    company_balance += float(company_cashbox.balance)
    return company_balance

def calculate_office_balance(office):
    office_balance = 0
    office_cashbox = OfficeCashbox.objects.get(office=office)
    office_balance += float(office_cashbox.balance)
    return office_balance

def create_cash_flow(
    holding=None, 
    company=None, 
    office=None, 
    date=datetime.date.today(), 
    operation_style=None, 
    description=None, 
    initial_balance=0, 
    subsequent_balance=0, 
    quantity=0, 
    executor=None,
    holding_initial_balance=0,
    holding_subsequent_balance=0,
    company_initial_balance=0,
    company_subsequent_balance=0,
    office_initial_balance=0,
    office_subsequent_balance=0,
):
    """
    Pul axinlarini create eden funksiya
    """

    cash_flow = CashFlow.objects.create(
        holding=holding,
        company=company,
        office=office,
        date=date,
        operation_style=operation_style,
        description=description,
        initial_balance=initial_balance,
        subsequent_balance=subsequent_balance,
        executor=executor,
        holding_initial_balance=holding_initial_balance,
        holding_subsequent_balance=holding_subsequent_balance,
        company_initial_balance=company_initial_balance,
        company_subsequent_balance=company_subsequent_balance,
        office_initial_balance=office_initial_balance,
        office_subsequent_balance=office_subsequent_balance,
        quantity=quantity
    )
    return cash_flow.save()
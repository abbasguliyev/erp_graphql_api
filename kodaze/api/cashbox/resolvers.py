from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow
)


def resolve_holding_cashbox(id):
    return HoldingCashbox.objects.select_related('holding').filter(id=id).first()


def resolve_holding_cashboxs():
    return HoldingCashbox.objects.select_related('holding').all()


def resolve_company_cashbox(id):
    return CompanyCashbox.objects.select_related('company').filter(id=id).first()


def resolve_company_cashboxs():
    return CompanyCashbox.objects.select_related('company').all()


def resolve_office_cashbox(id):
    return OfficeCashbox.objects.select_related('office').filter(id=id).first()


def resolve_office_cashboxs():
    return OfficeCashbox.objects.select_related('office').all()


def resolve_cash_flow(id):
    return CashFlow.objects.select_related('holding', 'company', 'office', 'executor').filter(id=id).first()


def resolve_cash_flows():
    return CashFlow.objects.select_related('holding', 'company', 'office', 'executor').all()

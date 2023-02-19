from contract.models import (
    Contract,
    ContractChange,
    ContractCreditor,
    ContractGift,
    DemoSales,
    Installment
)


def resolve_contract(id):
    return Contract.objects.select_related(
        "responsible_employee_1",
        "responsible_employee_2",
        "responsible_employee_3",
        "customer",
        "product",
        "company",
        "office"
    ).get(pk=id)


def resolve_contracts():
    return Contract.objects.select_related(
        "responsible_employee_1",
        "responsible_employee_2",
        "responsible_employee_3",
        "customer",
        "product",
        "company",
        "office"
    ).all()


def resolve_contract_change(id):
    return ContractChange.objects.select_related('old_contract', 'product').get(pk=id)


def resolve_contract_changes():
    return ContractChange.objects.select_related('old_contract', 'product').all()


def resolve_contract_creditor(id):
    return ContractCreditor.objects.select_related('creditor', 'contract').get(pk=id)


def resolve_contract_creditors():
    return ContractCreditor.objects.select_related('creditor', 'contract').all()


def resolve_contract_gift(id):
    return ContractGift.objects.select_related('contract', 'product').get(pk=id)


def resolve_contract_gifts():
    return ContractGift.objects.select_related('contract', 'product').all()


def resolve_demo_sale(id):
    return DemoSales.objects.select_related('user').get(pk=id)


def resolve_demo_sales():
    return DemoSales.objects.select_related('user').all()


def resolve_installment(id):
    return Installment.objects.select_related('contract').get(pk=id)


def resolve_installments():
    return Installment.objects.select_related('contract').all()

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from core.image_validator import file_size

USER = get_user_model()


class AbstractIncomeExpense(models.Model):
    amount = models.FloatField(default=0)
    image_of_receipt = models.ImageField(upload_to="media/%Y/%m/%d/", null=True, blank=True, validators=[
                                         file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    note = models.TextField(null=True, blank=True)
    date = models.DateField(default=None)
    previous_balance = models.FloatField(default=0, blank=True)
    subsequent_balance = models.FloatField(default=0, blank=True)

    class Meta:
        abstract = True


class HoldingCashboxIncome(AbstractIncomeExpense):
    image_of_receipt = None
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_holding_income")
    holding_cashbox = models.ForeignKey("cashbox.HoldingCashbox", on_delete=models.CASCADE, null=True,
                                        related_name="holding_cashbox_income")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_holdingcashboxincome",
             "Mövcud holdinq kassa mədaxillərə baxa bilər"),
            ("add_holdingcashboxincome", "Holdinq kassa mədaxil əlavə edə bilər"),
            ("change_holdingcashboxincome",
             "Holdinq kassa mədaxil məlumatlarını yeniləyə bilər"),
            ("delete_holdingcashboxincome", "Holdinq kassa mədaxil silə bilər")
        )


class HoldingCashboxExpense(AbstractIncomeExpense):
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_holding_expense")
    holding_cashbox = models.ForeignKey("cashbox.HoldingCashbox", on_delete=models.CASCADE, null=True,
                                        related_name="holding_cashbox_expense")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_holdingcashboxexpense",
             "Mövcud holdinq kassa məxariclərə baxa bilər"),
            ("add_holdingcashboxexpense", "Holdinq kassa məxaric əlavə edə bilər"),
            ("change_holdingcashboxexpense",
             "Holdinq kassa məxaric məlumatlarını yeniləyə bilər"),
            ("delete_holdingcashboxexpense", "Holdinq kassa məxaric silə bilər")
        )


# -----------------------------------------------------

class CompanyCashboxIncome(AbstractIncomeExpense):
    image_of_receipt = None
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_company_income")
    company_cashbox = models.ForeignKey("cashbox.CompanyCashbox", on_delete=models.CASCADE, null=True,
                                        related_name="company_cashbox_income")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_companycashboxincome",
             "Mövcud şirkət kassa mədaxillərə baxa bilər"),
            ("add_companycashboxincome", "Şirkət kassa mədaxil əlavə edə bilər"),
            ("change_companycashboxincome",
             "Şirkət kassa mədaxil məlumatlarını yeniləyə bilər"),
            ("delete_companycashboxincome", "Şirkət kassa mədaxil silə bilər")
        )


class CompanyCashboxExpense(AbstractIncomeExpense):
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_company_expense")
    company_cashbox = models.ForeignKey("cashbox.CompanyCashbox", on_delete=models.CASCADE, null=True,
                                        related_name="company_cashbox_expense")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_companycashboxexpense",
             "Mövcud şirkət kassa məxariclərə baxa bilər"),
            ("add_companycashboxexpense", "Şirkət kassa məxaric əlavə edə bilər"),
            ("change_companycashboxexpense",
             "Şirkət kassa məxaric məlumatlarını yeniləyə bilər"),
            ("delete_companycashboxexpense", "Şirkət kassa məxaric silə bilər")
        )

# -----------------------------------------------------


class OfficeKassaIncome(AbstractIncomeExpense):
    image_of_receipt = None
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_office_income")
    office_cashbox = models.ForeignKey(
        "cashbox.OfficeCashbox", on_delete=models.CASCADE, null=True, related_name="office_cashbox_income")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_officecashboxincome", "Mövcud office kassa mədaxillərə baxa bilər"),
            ("add_officecashboxincome", "Office kassa mədaxil əlavə edə bilər"),
            ("change_officecashboxincome",
             "Office kassa mədaxil məlumatlarını yeniləyə bilər"),
            ("delete_officecashboxincome", "Office kassa mədaxil silə bilər")
        )


class OfficeKassaExpense(AbstractIncomeExpense):
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,
                                 related_name="user_office_expense")
    office_cashbox = models.ForeignKey(
        "cashbox.OfficeCashbox", on_delete=models.CASCADE, null=True, related_name="office_cashbox_expense")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_officecashboxexpense",
             "Mövcud office kassa məxariclərə baxa bilər"),
            ("add_officecashboxexpense", "Office kassa məxaric əlavə edə bilər"),
            ("change_officecashboxexpense",
             "Office kassa məxaric məlumatlarını yeniləyə bilər"),
            ("delete_officecashboxexpense", "Office kassa məxaric silə bilər")
        )

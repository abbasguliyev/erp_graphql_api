import django
from django.db import models
import datetime
from django.contrib.auth import get_user_model

USER = get_user_model()


class AbstractPrim(models.Model):
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'
    ODENIS_USLUBU_CHOICES = [
        (KREDIT, "KREDİT"),
        (NAGD, "NƏĞD"),
    ]

    prim_status = models.ForeignKey(
        'account.EmployeeStatus', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=True, blank=True)
    sales_amount = models.FloatField(default=0, null=True, blank=True)
    payment_style = models.CharField(
        max_length=20,
        choices=ODENIS_USLUBU_CHOICES,
        default=NAGD
    )
    position = models.ForeignKey(
        'company.Position', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class AbstractSalaryMethod(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    date = models.DateField(default=django.utils.timezone.now, blank=True)

    class Meta:
        abstract = True


class VanLeaderPrimNew(AbstractPrim):
    payment_style = None
    cash = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_vanleaderprimnew", "Mövcud vanleader primlərə baxa bilər"),
            ("add_vanleaderprimnew", "Vanleader prim əlavə edə bilər"),
            ("change_vanleaderprimnew", "Vanleader prim məlumatlarını yeniləyə bilər"),
            ("delete_vanleaderprimnew", "Vanleader prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.position.name}"


class DealerPrimNew(AbstractPrim):
    payment_style = None
    cash = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_dealerprimnew", "Mövcud dealer primlərə baxa bilər"),
            ("add_dealerprimnew", "Dealer prim əlavə edə bilər"),
            ("change_dealerprimnew", "Dealer prim məlumatlarını yeniləyə bilər"),
            ("delete_dealerprimnew", "Dealer prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.position.name}"


class OfficeLeaderPrim(AbstractPrim):
    payment_style = None
    prim_for_office = models.FloatField(default=0, blank=True)
    fix_prim = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officeleaderprim", "Mövcud office leader primlərə baxa bilər"),
            ("add_officeleaderprim", "Office Leader prim əlavə edə bilər"),
            ("change_officeleaderprim",
             "Office Leader prim məlumatlarını yeniləyə bilər"),
            ("delete_officeleaderprim", "Office Leader prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.prim_for_office} - {self.position.name}"


class CanvasserPrim(AbstractPrim):
    payment_style = None
    sale_0 = models.FloatField(default=0, blank=True)
    sale_1_8 = models.FloatField(default=0, blank=True)
    sale_9_14 = models.FloatField(default=0, blank=True)
    sale_15p = models.FloatField(default=0, blank=True)
    sale_20p = models.FloatField(default=0, blank=True)
    prim_for_team = models.FloatField(default=0, blank=True)
    prim_for_office = models.FloatField(default=0, blank=True)
    fix_prim = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_canvasserprim", "Mövcud canvasser primlərə baxa bilər"),
            ("add_canvasserprim", "Canvasser prim əlavə edə bilər"),
            ("change_canvasserprim", "Canvasser prim məlumatlarını yeniləyə bilər"),
            ("delete_canvasserprim", "Canvasser prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.prim_for_office} - {self.position.name}"


class CreditorPrim(models.Model):
    prim_percent = models.PositiveBigIntegerField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_creditorprim", "Mövcud kreditor primlərə baxa bilər"),
            ("add_creditorprim", "Kreditor prim əlavə edə bilər"),
            ("change_creditorprim", "Kreditor prim məlumatlarını yeniləyə bilər"),
            ("delete_creditorprim", "Kreditor prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_percent}"

# -----------------------------------------------------------------------------------------------------------------------------


class AdvancePayment(AbstractSalaryMethod):
    half_month_salary = models.PositiveBigIntegerField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_advancepayment", "Mövcud avanslara baxa bilər"),
            ("add_advancepayment", "Avans əlavə edə bilər"),
            ("change_advancepayment", "Avans məlumatlarını yeniləyə bilər"),
            ("delete_advancepayment", "Avans silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.date}"


class PaySalary(AbstractSalaryMethod):
    installment = models.DateField(
        default=django.utils.timezone.now, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_paysalary", "Mövcud maaş ödəmələrinə baxa bilər"),
            ("add_paysalary", "Maaş ödəmə əlavə edə bilər"),
            ("change_paysalary", "Maaş ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_paysalary", "Maaş ödəmə silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.installment}"


class SalaryDeduction(AbstractSalaryMethod):

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salarydeduction", "Mövcud kəsintilərə baxa bilər"),
            ("add_salarydeduction", "Kəsinti əlavə edə bilər"),
            ("change_salarydeduction", "Kəsinti məlumatlarını yeniləyə bilər"),
            ("delete_salarydeduction", "Kəsinti silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.date}"


class Bonus(AbstractSalaryMethod):

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_bonus", "Mövcud bonuslara baxa bilər"),
            ("add_bonus", "Bonus əlavə edə bilər"),
            ("change_bonus", "Bonus məlumatlarını yeniləyə bilər"),
            ("delete_bonus", "Bonus silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.amount} {self.date}"


class SalaryView(models.Model):
    employee = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="employee_salary_views")
    sales_quantity = models.PositiveBigIntegerField(default=0, blank=True)
    sales_amount = models.FloatField(default=0, blank=True)
    final_salary = models.FloatField(default=0, blank=True)
    date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salaryview", "Mövcud maaş cədvəllərinə baxa bilər"),
            ("add_salaryview", "Maaş cədvəli əlavə edə bilər"),
            ("change_salaryview", "Maaş cədvəlinin məlumatlarını yeniləyə bilər"),
            ("delete_salaryview", "Maaş cədvəlini silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.final_salary} {self.date}"

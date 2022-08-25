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

    prim_status = models.ForeignKey('account.EmployeeStatus', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True, blank=True)
    sales_amount = models.FloatField(default=0, null=True, blank=True)
    payment_style =  models.CharField(
        max_length=20,
        choices=ODENIS_USLUBU_CHOICES,
        default=NAGD
    )
    position = models.ForeignKey('company.Position', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

class VanLeaderPrim(AbstractPrim):
    teamya_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.teamya_gore_prim} - {self.payment_style} - {self.position.name}"

class VanLeaderPrimNew(AbstractPrim):
    payment_style = None
    negd = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_person_in_charge_1primnew", "Mövcud person_in_charge_1 primlərə baxa bilər"),
            ("add_person_in_charge_1primnew", "Vanleader prim əlavə edə bilər"),
            ("change_person_in_charge_1primnew", "Vanleader prim məlumatlarını yeniləyə bilər"),
            ("delete_person_in_charge_1primnew", "Vanleader prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.position.name}"

class DealerPrim(AbstractPrim):
    teamya_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.teamya_gore_prim} - {self.payment_style} - {self.position.name}"

class DealerPrimNew(AbstractPrim):
    payment_style = None
    negd = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_person_in_charge_2primnew", "Mövcud person_in_charge_2 primlərə baxa bilər"),
            ("add_person_in_charge_2primnew", "Dealer prim əlavə edə bilər"),
            ("change_person_in_charge_2primnew", "Dealer prim məlumatlarını yeniləyə bilər"),
            ("delete_person_in_charge_2primnew", "Dealer prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.position.name}"

class OfficeLeaderPrim(AbstractPrim):
    payment_style = None
    officee_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officeleaderprim", "Mövcud office leader primlərə baxa bilər"),
            ("add_officeleaderprim", "Office Leader prim əlavə edə bilər"),
            ("change_officeleaderprim", "Office Leader prim məlumatlarını yeniləyə bilər"),
            ("delete_officeleaderprim", "Office Leader prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_status} - {self.officee_gore_prim} - {self.position.name}"

class CanvasserPrim(AbstractPrim):
    payment_style = None
    satis0 = models.FloatField(default=0, blank=True)
    satis1_8 = models.FloatField(default=0, blank=True)
    satis9_14 = models.FloatField(default=0, blank=True)
    satis15p = models.FloatField(default=0, blank=True)
    satis20p = models.FloatField(default=0, blank=True)
    teamya_gore_prim = models.FloatField(default=0, blank=True)
    officee_gore_prim = models.FloatField(default=0, blank=True)
    fix_maas = models.FloatField(default=0, blank=True)

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
        return f"{self.prim_status} - {self.officee_gore_prim} - {self.position.name}"

class KreditorPrim(models.Model):
    prim_faizi = models.PositiveBigIntegerField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_installmentorprim", "Mövcud installmentor primlərə baxa bilər"),
            ("add_installmentorprim", "Kreditor prim əlavə edə bilər"),
            ("change_installmentorprim", "Kreditor prim məlumatlarını yeniləyə bilər"),
            ("delete_installmentorprim", "Kreditor prim silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.prim_faizi}"

# -----------------------------------------------------------------------------------------------------------------------------

class Avans(models.Model):
    employee = models.ManyToManyField(USER, related_name="employee_avans")
    amount = models.FloatField(default=0, blank=True)
    yarim_ay_emek_haqqi = models.PositiveBigIntegerField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    avans_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_avans", "Mövcud avanslara baxa bilər"),
            ("add_avans", "Avans əlavə edə bilər"),
            ("change_avans", "Avans məlumatlarını yeniləyə bilər"),
            ("delete_avans", "Avans silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.avans_tarixi}"

class MaasOde(models.Model):
    employee = models.ManyToManyField(USER, related_name="maas_ode")
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    installment = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_maasode", "Mövcud maaş ödəmələrinə baxa bilər"),
            ("add_maasode", "Maaş ödəmə əlavə edə bilər"),
            ("change_maasode", "Maaş ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_maasode", "Maaş ödəmə silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.installment}"

class Kesinti(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="employee_kesinti")
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    kesinti_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_kesinti", "Mövcud kəsintilərə baxa bilər"),
            ("add_kesinti", "Kəsinti əlavə edə bilər"),
            ("change_kesinti", "Kəsinti məlumatlarını yeniləyə bilər"),
            ("delete_kesinti", "Kəsinti silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.kesinti_tarixi}"

class Bonus(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="employee_bonus")
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    bonus_tarixi = models.DateField(default=django.utils.timezone.now, blank=True)
    
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
        return f"{self.employee} {self.amount} {self.bonus_tarixi}"
 
class MaasGoruntuleme(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="employee_maas_goruntuleme")
    satis_quantityi = models.PositiveBigIntegerField(default=0, blank=True)
    sales_amount = models.FloatField(default=0, blank=True)
    yekun_maas = models.FloatField(default=0, blank=True)
    date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_maasgoruntuleme", "Mövcud maaş cədvəllərinə baxa bilər"),
            ("add_maasgoruntuleme", "Maaş cədvəli əlavə edə bilər"),
            ("change_maasgoruntuleme", "Maaş cədvəlinin məlumatlarını yeniləyə bilər"),
            ("delete_maasgoruntuleme", "Maaş cədvəlini silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} {self.yekun_maas} {self.date}"
from django.db import models
import django
from core.image_validator import file_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.


class Contract(models.Model):
    INSTALLMENT = 'KREDİT'
    CASH = 'NƏĞD'

    PAYMENT_STYLE_CHOICES = [
        (CASH, "NƏĞD"),
        (INSTALLMENT, "KREDİT")
    ]

    CONTINUING = "DAVAM EDƏN"
    FINISHED = "BİTMİŞ"
    CANCELLED = "DÜŞƏN"
    NONE = "YOXDUR"
    NEW_GRAPH = "YENİ QRAFİK"

    NEW_GRAPH_CHOICES = [
        (NEW_GRAPH, "YENİ QRAFİK")
    ]

    CONTRACT_STATUS_CHOICES = [
        (CONTINUING, "DAVAM EDƏN"),
        (FINISHED, "BİTMİŞ"),
        (CANCELLED, "DÜŞƏN")
    ]

    INITIAL_PAYMENT_STATUS_CHOICES = [
        (NONE, "YOXDUR"),
        (FINISHED, "BİTMİŞ"),
        (CONTINUING, "DAVAM EDƏN"),
    ]

    INITIAL_PAYMENT_DEBT_STATUS_CHOICES = [
        (NONE, "YOXDUR"),
        (FINISHED, "BİTMİŞ"),
        (CONTINUING, "DAVAM EDƏN"),
    ]

    MODIFIED_PRODUCT = "DƏYİŞİLMİŞ MƏHSUL"

    MODIFIED_PRODUCT_STATUS_CHOICES = [
        (MODIFIED_PRODUCT, "DƏYİŞİLMİŞ MƏHSUL")
    ]

    person_in_charge_1 = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="person_in_charge_1", null=True, blank=True)
    person_in_charge_2 = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="person_in_charge_2", null=True, blank=True)
    person_in_charge_3 = models.ForeignKey(
        'account.User', on_delete=models.CASCADE, related_name="person_in_charge_3", null=True, blank=True)
    customer = models.ForeignKey('account.Cutomer', on_delete=models.CASCADE, related_name="contracts", null=True,
                                 blank=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="contracts", null=True,
                                blank=True)
    product_quantity = models.PositiveIntegerField(default=1, blank=True)
    total_amount = models.FloatField(default=0, blank=True)
    electronic_signature = models.ImageField(upload_to="media/contract/%Y/%m/%d/", null=True, blank=True, validators=[
                                             file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    contract_date = models.DateField(null=True, blank=True)
    contract_created_date = models.DateField(auto_now_add=True, null=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE,
                                related_name="contracts", null=True, blank=True)
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE,
                               related_name="contracts", null=True, blank=True)
    remaining_debt = models.FloatField(default=0, blank=True)
    is_remove = models.BooleanField(default=False)

    payment_style = models.CharField(
        max_length=20,
        choices=PAYMENT_STYLE_CHOICES,
        default=CASH
    )

    new_graphic_amount = models.FloatField(default=0, blank=True)
    new_graphic_status = models.CharField(
        max_length=50,
        choices=NEW_GRAPH_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    modified_product_status = models.CharField(
        max_length=50,
        choices=MODIFIED_PRODUCT_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    contract_status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default=CONTINUING
    )

    loan_term = models.IntegerField(default=0, blank=True)
    initial_payment = models.FloatField(blank=True, default=0)
    initial_payment_debt = models.FloatField(blank=True, default=0)
    initial_payment_date = models.DateField(blank=True, null=True)
    initial_payment_debt_date = models.DateField(blank=True, null=True)

    initial_payment_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_STATUS_CHOICES,
        default=NONE
    )

    initial_payment_debt_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_DEBT_STATUS_CHOICES,
        default=NONE
    )
    pdf = models.FileField(upload_to="media/contract/%Y/%m/%d/", blank=True,
                           null=True, validators=[file_size, FileExtensionValidator(['pdf'])])
    pdf2 = models.FileField(upload_to="media/contract/%Y/%m/%d/", blank=True,
                            null=True, validators=[file_size, FileExtensionValidator(['pdf'])])

    cancelled_date = models.DateField(null=True, blank=True)
    debt_closing_date = models.DateField(null=True, blank=True)

    compensation_income = models.FloatField(default=0, null=True, blank=True)
    compensation_expense = models.FloatField(default=0, null=True, blank=True)

    debt_finished = models.BooleanField(default=False, blank=True)

    creditor = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="creditor_contracts")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contract", "Mövcud müqavilələrə baxa bilər"),
            ("add_contract", "Müqavilə əlavə edə bilər"),
            ("change_contract", "Müqavilə məlumatlarını yeniləyə bilər"),
            ("delete_contract", "Müqavilə silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.pk}. contract {self.customer} - {self.product}"


class ContractGift(models.Model):
    product = models.ManyToManyField("product.Product", related_name="gifts")
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="gifts")
    quantity = models.PositiveBigIntegerField(default=1)
    gift_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_contractgift", "Mövcud müqavilə hədiyyələrə baxa bilər"),
            ("add_contractgift", "Müqavilə hədiyyə əlavə edə bilər"),
            ("change_contractgift", "Müqavilə hədiyyə məlumatlarını yeniləyə bilər"),
            ("delete_contractgift", "Müqavilə hədiyyə silə bilər")
        )

    def __str__(self) -> str:
        return f"Gift --- {self.contract} - {self.product}"


class INSTALLMENT(models.Model):
    ODENEN = "ÖDƏNƏN"
    ODENMEYEN = "ÖDƏNMƏYƏN"

    BURAXILMIS_AY = "BURAXILMIŞ AY"
    NATAMAM_AY = "NATAMAM AY"
    RAZILASDIRILMIS_AZ_ODEME = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
    ARTIQ_ODEME = "ARTIQ ÖDƏMƏ"
    SON_AYIN_BOLUNMESI = "SON AYIN BÖLÜNMƏSİ"

    GECIKDIRME = "GECİKDİRMƏ"

    SIFIR_NOVBETI_AY = "SIFIR NÖVBƏTİ AY"
    SIFIR_SONUNCU_AY = "SIFIR SONUNCU AY"
    SIFIR_DIGER_AYLAR = "SIFIR DİGƏR AYLAR"

    NATAMAM_NOVBETI_AY = "NATAMAM NÖVBƏTİ AY"
    NATAMAM_SONUNCU_AY = "NATAMAM SONUNCU AY"
    NATAMAM_DIGER_AYLAR = "NATAMAM DİGƏR AYLAR"

    ARTIQ_BIR_AY = "ARTIQ BİR AY"
    ARTIQ_BUTUN_AYLAR = "ARTIQ BÜTÜN AYLAR"

    BORCU_BAGLA = "BORCU BAĞLA"

    ODEME_STATUS_CHOICES = [
        (ODENMEYEN, "ÖDƏNMƏYƏN"),
        (ODENEN, "ÖDƏNƏN"),
    ]

    SERTLI_ODEME_STATUSU = [
        (BURAXILMIS_AY, "BURAXILMIŞ AY"),
        (NATAMAM_AY, "NATAMAM AY"),
        (RAZILASDIRILMIS_AZ_ODEME, "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"),
        (ARTIQ_ODEME, "ARTIQ ÖDƏMƏ"),
        (SON_AYIN_BOLUNMESI, "SON AYIN BÖLÜNMƏSİ")
    ]

    GECIKDIRME_STATUS_CHOICES = [
        (GECIKDIRME, "GECİKDİRMƏ")
    ]

    SIFIR_STATUS_CHOICES = [
        (SIFIR_NOVBETI_AY, "SIFIR NÖVBƏTİ AY"),
        (SIFIR_SONUNCU_AY, "SIFIR SONUNCU AY"),
        (SIFIR_DIGER_AYLAR, "SIFIR DİGƏR AYLAR")
    ]

    NATAMAM_STATUS_CHOICES = [
        (NATAMAM_NOVBETI_AY, "NATAMAM NÖVBƏTİ AY"),
        (NATAMAM_SONUNCU_AY, "NATAMAM SONUNCU AY"),
        (NATAMAM_DIGER_AYLAR, "NATAMAM DİGƏR AYLAR")
    ]

    ARTIQ_ODEME_STATUS_CHOICES = [
        (ARTIQ_BIR_AY, "ARTIQ BİR AY"),
        (ARTIQ_BUTUN_AYLAR, "ARTIQ BÜTÜN AYLAR")
    ]

    BORCU_BAGLA_STATUS_CHOICES = [
        (BORCU_BAGLA, "BORCU BAĞLA")
    ]

    month_no = models.PositiveIntegerField(default=1)
    contract = models.ForeignKey(Contract, blank=True, null=True, related_name='installments',
                                 on_delete=models.CASCADE)
    date = models.DateField(default=False, blank=True, null=True)
    price = models.FloatField(default=0, blank=True)
    payment_status = models.CharField(
        max_length=30,
        choices=ODEME_STATUS_CHOICES,
        default=ODENMEYEN
    )

    contingent_payment_status = models.CharField(
        max_length=50,
        choices=SERTLI_ODEME_STATUSU,
        default=None,
        null=True,
        blank=True
    )

    close_the_debt_status = models.CharField(
        max_length=30,
        choices=BORCU_BAGLA_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    delay_status = models.CharField(
        max_length=30,
        choices=GECIKDIRME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    missed_month_substatus = models.CharField(
        max_length=20,
        choices=SIFIR_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    incomplete_month_substatus = models.CharField(
        max_length=20,
        choices=NATAMAM_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    overpayment_substatus = models.CharField(
        max_length=20,
        choices=ARTIQ_ODEME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    last_month = models.BooleanField(default=False)
    note = models.TextField(default="", blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_installment", "Mövcud ödəmələrə baxa bilər"),
            ("add_installment", "Ödəmə əlavə edə bilər"),
            ("change_installment", "Ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_installment", "Ödəmə silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.pk}. {self.month_no}.month-{self.date} - ({self.contract.id}).id contract - {self.contract.customer.asa} - {self.price}"


class ContractChange(models.Model):
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'

    ODENIS_USLUBU_CHOICES = [
        (NAGD, "NƏĞD"),
        (KREDIT, "KREDİT"),
    ]
    old_contract = models.ForeignKey(
        Contract, related_name="changed_contracts", on_delete=models.CASCADE)
    payment_style = models.CharField(
        max_length=100, choices=ODENIS_USLUBU_CHOICES, default=KREDIT)
    loan_term = models.PositiveIntegerField(default=0, blank=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contractchange", "Mövcud dəyişimlərə baxa bilər"),
            ("add_contractchange", "Dəyişim əlavə edə bilər"),
            ("change_contractchange", "Dəyişim məlumatlarını yeniləyə bilər"),
            ("delete_contractchange", "Dəyişim silə bilər")
        )


class DemoSales(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="demos")
    count = models.IntegerField(default=0)
    created_date = models.DateField(
        default=django.utils.timezone.now, blank=True)
    sale_count = models.IntegerField(default=0)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_demosales", "Mövcud demo satışlara baxa bilər"),
            ("add_demosales", "Demo satış əlavə edə bilər"),
            ("change_demosales", "Demo satış məlumatlarını yeniləyə bilər"),
            ("delete_demosales", "Demo satış silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.user.username}-{self.count} demo - {self.created_date}"
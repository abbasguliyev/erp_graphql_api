import django
from django.db import models

# Create your models here.


class Service(models.Model):
    installment = models.BooleanField(default=False, blank=True)
    loan_term = models.IntegerField(default=0, blank=True)
    discount = models.FloatField(default=0, blank=True)
    contract = models.ForeignKey(
        "contract.Contract", related_name="services", null=True, on_delete=models.CASCADE)
    product = models.ManyToManyField(
        "product.Product", related_name="services")
    service_date = models.DateField(
        default=django.utils.timezone.now, blank=True)
    is_done = models.BooleanField(default=False)
    price = models.FloatField(default=0, blank=True)
    initial_payment = models.FloatField(default=0, blank=True)
    total_amount_to_be_paid = models.FloatField(default=0, blank=True)
    confirmation = models.BooleanField(default=False)
    note = models.TextField(default="", blank=True)
    is_auto = models.BooleanField(default=False)
    create_date = models.DateField(
        default=django.utils.timezone.now, editable=False)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_service", "Mövcud servislərə baxa bilər"),
            ("add_service", "Servis əlavə edə bilər"),
            ("change_service", "Servis məlumatlarını yeniləyə bilər"),
            ("delete_service", "Servis silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.pk}.service-{self.contract}"


class ServicePayment(models.Model):
    service = models.ForeignKey(
        Service, related_name="service_payment", null=True, on_delete=models.CASCADE)
    total_amount_to_be_paid = models.FloatField(default=0, blank=True)
    amount_to_be_paid = models.FloatField(default=0, blank=True)
    is_done = models.BooleanField(default=False)
    payment_date = models.DateField(
        default=django.utils.timezone.now, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_servicepayment", "Mövcud service ödəmələrinə baxa bilər"),
            ("add_servicepayment", "Service ödəmə əlavə edə bilər"),
            ("change_servicepayment", "Service ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_servicepayment", "Service ödəmə silə bilər")
        )

    def __str__(self) -> str:
        return f"service-{self.service}-{self.amount_to_be_paid}-{self.is_done}"

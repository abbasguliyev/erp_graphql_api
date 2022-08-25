import django
from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import User
from core.image_validator import file_size
from django.contrib.auth import get_user_model

User = get_user_model()


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    office = models.ForeignKey(
        'company.Office', on_delete=models.CASCADE, null=True, related_name="warehouses")
    company = models.ForeignKey(
        'company.Company', on_delete=models.CASCADE, null=True, related_name="warehouses")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_warehouse", "Mövcud anbarlara baxa bilər"),
            ("add_warehouse", "Anbar əlavə edə bilər"),
            ("change_warehouse", "Anbar məlumatlarını yeniləyə bilər"),
            ("delete_warehouse", "Anbar silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.name} - {self.office}"


class WarehouseRequest(models.Model):
    employee_who_sent_the_request = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="warehouse_requests")
    product_and_quantity = models.CharField(
        max_length=250, null=True, blank=True)
    note = models.TextField()
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="warehouse_note")
    is_done = models.BooleanField(default=False)
    request_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_warehouserequest", "Mövcud anbar sorğularına baxa bilər"),
            ("add_warehouserequest", "Anbar sorğu əlavə edə bilər"),
            ("change_warehouserequest", "Anbar sorğu məlumatlarını yeniləyə bilər"),
            ("delete_warehouserequest", "Anbar sorğu silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.warehouse} - {self.note[:30]}"


class Stock(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.CASCADE, related_name="stocks")
    product = models.ForeignKey(
        "product.Product", null=True, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.IntegerField(default=0)
    date = models.DateField(auto_now=True, blank=True)
    note = models.TextField(default="", null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_stock", "Mövcud stoklara baxa bilər"),
            ("add_stock", "Stok əlavə edə bilər"),
            ("change_stock", "Stok məlumatlarını yeniləyə bilər"),
            ("delete_stock", "Stok silə bilər")
        )

    def __str__(self) -> str:
        return f"stock -> {self.warehouse} - {self.product} - {self.quantity}"


class Operation(models.Model):
    TRANSFER = 'transfer'
    STOK_YENILEME = 'stok yeniləmə'

    EMELIYYAT_NOVU_CHOICES = [
        (TRANSFER, "transfer"),
        (STOK_YENILEME, "stok yeniləmə"),
    ]

    shipping_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, related_name="shipping_warehouse")
    receiving_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, related_name="receiving_warehouse")

    product_and_quantity = models.CharField(
        max_length=500, null=True, blank=True)

    note = models.TextField(default="", null=True, blank=True)
    operation_date = models.DateField(
        auto_now_add=True, null=True, blank=True)

    operation_type = models.CharField(
        max_length=50, choices=EMELIYYAT_NOVU_CHOICES, default=TRANSFER)

    quantity = models.IntegerField(default=0, blank=True, null=True)
    executor = models.ForeignKey(
        User, related_name="operations", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_operation", "Mövcud əməliyyatlara baxa bilər"),
            ("add_operation", "Əməliyyat əlavə edə bilər"),
            ("change_operation", "Əməliyyat məlumatlarını yeniləyə bilər"),
            ("delete_operation", "Əməliyyat silə bilər")
        )

    def __str__(self) -> str:
        return f"Operation ==> {self.shipping_warehouse} - {self.receiving_warehouse} {self.operation_date}"

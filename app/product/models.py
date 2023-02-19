from django.db import models
from django.db.models import (
    F
)
from django.core.validators import FileExtensionValidator
from core.image_validator import file_size


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_unitofmeasure", "Mövcud ölçü vahidlərinə baxa bilər"),
            ("add_unitofmeasure", "Ölçü vahidi əlavə edə bilər"),
            ("change_unitofmeasure", "Ölçü vahidi məlumatlarını yeniləyə bilər"),
            ("delete_unitofmeasure", "Ölçü vahidini silə bilər")
        )

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_category", "Mövcud kateqoriyalara baxa bilər"),
            ("add_category", "Kateqoriya əlavə edə bilər"),
            ("change_category", "Kateqoriya məlumatlarını yeniləyə bilər"),
            ("delete_category", "Kateqoriya silə bilər")
        )

    def __str__(self) -> str:
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    company = models.ForeignKey(
        'company.Company', on_delete=models.CASCADE, null=True, related_name="products")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="products")
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, on_delete=models.SET_NULL, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    product_image = models.ImageField(upload_to="media/product/%Y/%m/%d/", null=True,
                                      blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    is_gift = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_product", "Mövcud məhsullara baxa bilər"),
            ("add_product", "Məhsul əlavə edə bilər"),
            ("change_product", "Məhsul məlumatlarını yeniləyə bilər"),
            ("delete_product", "Məhsul silə bilər")
        )

    @property
    def box_volume(self, *args, **kwargs):
        self.volume = F("weight") * F("width") * F("length")
        self.save(update_fields=["volume"])

    def __str__(self) -> str:
        return f"{self.company.name} company {self.product_name} - {self.price}"

from unicodedata import category
from django.db import models


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
    price = models.FloatField()
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_product", "Mövcud məhsullara baxa bilər"),
            ("add_product", "Məhsul əlavə edə bilər"),
            ("change_product", "Məhsul məlumatlarını yeniləyə bilər"),
            ("delete_product", "Məhsul silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.company.company_name} company {self.product_name} - {self.price}"

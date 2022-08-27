from django.db import models
from django.contrib.auth.models import Group

from django.core.validators import FileExtensionValidator
from core.image_validator import file_size

from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.
class AbstractCompany(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, blank=True)
    
    class Meta:
        abstract = True

class Holding(AbstractCompany):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holding", "Mövcud holdinqlərə baxa bilər"),
            ("add_holding", "Holdinq əlavə edə bilər"),
            ("change_holding", "Holdinq məlumatlarını yeniləyə bilər"),
            ("delete_holding", "Holdinq silə bilər")
        )

    def __str__(self) -> str:
        return self.name


class Company(AbstractCompany):
    name = models.CharField(max_length=200, unique=True)
    holding = models.ForeignKey(
        Holding, on_delete=models.CASCADE, related_name="companies")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_company", "Mövcud şirkətlərə baxa bilər"),
            ("add_company", "Şirkət əlavə edə bilər"),
            ("change_company", "Şirkət məlumatlarını yeniləyə bilər"),
            ("delete_company", "Şirkət silə bilər")
        )

    def __str__(self) -> str:
        return self.name


class Office(AbstractCompany):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="offices")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_office", "Mövcud ofislərə baxa bilər"),
            ("add_office", "Ofis əlavə edə bilər"),
            ("change_office", "Ofis məlumatlarını yeniləyə bilər"),
            ("delete_office", "Ofis silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.name} - {self.company}"


class Department(AbstractCompany):
    office = models.ForeignKey(
        Office, on_delete=models.CASCADE, null=True, related_name="departments")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_department", "Mövcud şöbələrə baxa bilər"),
            ("add_department", "Şöbə əlavə edə bilər"),
            ("change_department", "Şöbə məlumatlarını yeniləyə bilər"),
            ("delete_department", "Şöbə silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.name} - {self.office}"


class Position(AbstractCompany):
    name = models.CharField(max_length=200, unique=True)
    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        return super(Position, self).save(*args, **kwargs)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_position", "Mövcud vəzifələrə baxa bilər"),
            ("add_position", "Vəzifə əlavə edə bilər"),
            ("change_position", "Vəzifə məlumatlarını yeniləyə bilər"),
            ("delete_position", "Vəzifə silə bilər")
        )

    def __str__(self):
        return f"{self.name}"


class Team(AbstractCompany):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_team", "Mövcud komandalara baxa bilər"),
            ("add_team", "Komanda əlavə edə bilər"),
            ("change_team", "Komanda məlumatlarını yeniləyə bilər"),
            ("delete_team", "Komanda silə bilər")
        )

    def __str__(self):
        return self.name


class PermissionForPosition(models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="permission_for_positions")
    permission_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="permission_for_positions")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_permissionforposition", "Mövcud Vəzifə icazələrinə baxa bilər"),
            ("add_permissionforposition", "Vəzifə icazə əlavə edə bilər"),
            ("change_permissionforposition", "Vəzifə icazə məlumatlarını yeniləyə bilər"),
            ("delete_permissionforposition", "Vəzifə icazə məlumatlarını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.position}-{self.permission_group}"


class AppLogo(models.Model):
    logo = models.ImageField(upload_to="media/logo/%Y/%m/%d/", null=True, blank=True,
                             validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])

    class Meta:
        default_permissions = []
        permissions = (
            ("view_applogo", "Logoya baxa bilər"),
            ("add_applogo", "Logo əlavə edə bilər"),
            ("change_applogo", "Logonu yeniləyə bilər"),
            ("delete_applogo", "Logonu silə bilər")
        )
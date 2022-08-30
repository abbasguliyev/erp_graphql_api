from django.db import models
import django
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager
from core.image_validator import file_size
from . import (
    CONTRACT_TYPE_CHOICES,
    SALARY_STYLE_CHOICES,
    MONTHLY,
    CUSTOMER_TYPE_CHOICES,
    STANDART,
)
from django.db.models import F


class EmployeeStatus(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.status_name

    def save(self, *args, **kwargs) -> None:
        self.status_name = self.status_name.upper()
        super(EmployeeStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeestatus", "Mövcud işçi statuslarına baxa bilər"),
            ("add_employeestatus", "İşçi statusu əlavə edə bilər"),
            ("change_employeestatus", "İşçi statusu məlumatlarını yeniləyə bilər"),
            ("delete_employeestatus", "İşçi statusunu silə bilər")
        )


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    start_date_of_work = models.DateField(
        default=django.utils.timezone.now, null=True, blank=True)
    dismissal_date = models.DateField(null=True, blank=True)
    phone_number_1 = models.CharField(max_length=200)
    phone_number_2 = models.CharField(max_length=200, null=True, blank=True)
    photo_ID = models.ImageField(upload_to="media/employee/%Y/%m/%d/", null=True,
                                 blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    back_photo_of_ID = models.ImageField(upload_to="media/employee/%Y/%m/%d/", null=True,
                                         blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    driving_license_photo = models.ImageField(upload_to="media/employee/%Y/%m/%d/", null=True, blank=True, validators=[
                                              file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    company = models.ForeignKey("company.Company", on_delete=models.SET_NULL,
                                related_name="employees", null=True, blank=True)
    office = models.ForeignKey("company.Office", on_delete=models.SET_NULL,
                               related_name="employees", null=True, blank=True)
    department = models.ForeignKey(
        "company.Department", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    position = models.ForeignKey(
        "company.Position", on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    team = models.OneToOneField("company.Team", default=None, on_delete=models.SET_NULL,
                                related_name="employees", null=True, blank=True)
    employee_status = models.ForeignKey(
        EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True)
    salary_style = models.CharField(
        max_length=50,
        choices=SALARY_STYLE_CHOICES,
        default=MONTHLY
    )
    contract_type = models.CharField(
        max_length=50,
        choices=CONTRACT_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True
    )
    salary = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/employee/%Y/%m/%d/", null=True,
                                      blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    supervisor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ("pk",)
        default_permissions = ()
        permissions = (
            ("view_user", "Mövcud işçilərə baxa bilər"),
            ("add_user", "İşçi əlavə edə bilər"),
            ("change_user", "İşçi məlumatlarını yeniləyə bilər"),
            ("delete_user", "İşçi silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.username}"


class Region(models.Model):
    region_name = models.CharField(max_length=300, unique=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_region", "Mövcud bölgələrə baxa bilər"),
            ("add_region", "Bölgə əlavə edə bilər"),
            ("change_region", "Bölgə məlumatlarını yeniləyə bilər"),
            ("delete_region", "Bölgə silə bilər")
        )

    def __str__(self) -> str:
        return self.region_name


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, default="", blank=True)
    profile_image = models.ImageField(upload_to="media/customer/%Y/%m/%d/", null=True,
                                      blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    photo_ID = models.ImageField(upload_to="media/customer/%Y/%m/%d/", null=True,
                                 blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    back_photo_of_ID = models.ImageField(upload_to="media/customer/%Y/%m/%d/", null=True,
                                         blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    phone_number_1 = models.CharField(max_length=50)
    phone_number_2 = models.CharField(max_length=50, null=True, blank=True)
    phone_number_3 = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="customers")
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    customer_type = models.CharField(
        max_length=50,
        choices=CUSTOMER_TYPE_CHOICES,
        default=STANDART,
        null=True,
        blank=True
    )
    order_count = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_customer", "Mövcud müştərilərə baxa bilər"),
            ("add_customer", "Müştəri əlavə edə bilər"),
            ("change_customer", "Müştəri məlumatlarını yeniləyə bilər"),
            ("delete_customer", "Müştəri silə bilər")
        )

    def increase_order_count(self, quantity: int = 1):
        self.order_count = F("order_count") + quantity
        self.save(update_fields=["order_count"])

    def decrease_order_count(self, quantity: int = 1):
        self.order_count = F("order_count") - quantity
        self.save(update_fields=["order_count"])

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.father_name}"


class CustomerNote(models.Model):
    note = models.TextField()
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="notes")
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_customernote", "Mövcud müştəri qeydlərinə baxa bilər"),
            ("add_customernote", "Müştəri qeydi əlavə edə bilər"),
            ("change_customernote", "Müştəri qeydinin məlumatlarını yeniləyə bilər"),
            ("delete_customernote", "Müştəri qeydlərini silə bilər")
        )

    def __str__(self):
        return f"{self.customer} -- {self.note[:20]}"

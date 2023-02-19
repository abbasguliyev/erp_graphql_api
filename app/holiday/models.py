from django.db import models
import pandas as pd
from datetime import datetime
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.
class ExceptionWorker(models.Model):
    exception_workers = models.ManyToManyField(USER, blank=True)
    holidays = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True
        
class AbstractWorkingDays(models.Model):
    working_days_count = models.PositiveBigIntegerField(default=0)
    non_working_days_count = models.PositiveBigIntegerField(default=0)
    holidays = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateField(default=datetime.now, blank=True)
    
    class Meta:
        abstract = True
        
class EmployeeArrivalAndDepartureTimes(models.Model):
    employee = models.ManyToManyField(USER, related_name="arrival_and_departure_times")
    arrival_time = models.TimeField()
    departure_time = models.TimeField()

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_employeearrivalanddeparturetimes", "Mövcud işçi gəlib-getmə vaxtlarına baxa bilər"),
            ("add_employeearrivalanddeparturetimes", "İşçi gəlib-getmə vaxtı əlavə edə bilər"),
            ("change_employeearrivalanddeparturetimes", "İşçi gəlib-getmə vaxtının məlumatlarını yeniləyə bilər"),
            ("delete_employeearrivalanddeparturetimes", "İşçi gəlib-getmə vaxtını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} - {self.arrival_time} - {self.departure_time}"


class EmployeeWorkingDay(AbstractWorkingDays):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="working_days")
    paid_leave_days = models.CharField(max_length=500, null=True, blank=True)
    unpaid_leave_days = models.CharField(max_length=500, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_amount = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_employeeworkingday", "Mövcud işçilərin tətil günlərinə baxa bilər"),
            ("add_employeeworkingday", "İşçilərə tətil günü əlavə edə bilər"),
            ("change_employeeworkingday", "İşçilərin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_employeeworkingday", "İşçilərin tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.employee} - {self.working_days_count} - {self.date}"

class HoldingWorkingDay(AbstractWorkingDays):
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, related_name="working_days")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingworkingday", "Mövcud holdinq tətil günlərinə baxa bilər"),
            ("add_holdingworkingday", "Holdinqə tətil günü əlavə edə bilər"),
            ("change_holdingworkingday", "Holdinqin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_holdingworkingday", "Holdinqin tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.holding} - {self.working_days_count} - {self.date}"


class CompanyWorkingDay(AbstractWorkingDays):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="working_days")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_companyworkingday", "Mövcud şirkət tətil günlərinə baxa bilər"),
            ("add_companyworkingday", "Şirkət tətil günü əlavə edə bilər"),
            ("change_companyworkingday", "Şirkətin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_companyworkingday", "Şirkətin tətil gününü silə bilər")
        )
  
    def __str__(self) -> str:
        return f"{self.company} - {self.working_days_count} - {self.date}"

class OfficeWorkingDay(AbstractWorkingDays):
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, related_name="working_days")
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officeworkingday", "Mövcud ofis tətil günlərinə baxa bilər"),
            ("add_officeworkingday", "Office tətil günü əlavə edə bilər"),
            ("change_officeworkingday", "Officein tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_officeworkingday", "Officein tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.office} - {self.working_days_count} - {self.date}"

class TeamWorkingDay(AbstractWorkingDays):
    team = models.ForeignKey('company.Team', on_delete=models.CASCADE, related_name="working_days")
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_teamworkingday", "Mövcud komanda tətil günlərinə baxa bilər"),
            ("add_teamworkingday", "Komanda tətil günü əlavə edə bilər"),
            ("change_teamworkingday", "Komandanın tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_teamworkingday", "Komandanın tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.team} - {self.working_days_count} - {self.date}"

class PositionWorkingDay(AbstractWorkingDays):
    position = models.ForeignKey('company.Position', on_delete=models.CASCADE, related_name="working_days")
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_positionworkingday", "Mövcud vəzifə tətil günlərinə baxa bilər"),
            ("add_positionworkingday", "Vəzifə tətil günü əlavə edə bilər"),
            ("change_positionworkingday", "Vəzifənin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_positionworkingday", "Vəzifənin tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.position} - {self.working_days_count} - {self.date}"

class DepartmentWorkingDay(AbstractWorkingDays):
    department = models.ForeignKey('company.Department', on_delete=models.CASCADE, related_name="working_days")
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_departmentworkingday", "Mövcud şöbə tətil günlərinə baxa bilər"),
            ("add_departmentworkingday", "Şöbə tətil günü əlavə edə bilər"),
            ("change_departmentworkingday", "Şöbənin tətil günü məlumatlarını yeniləyə bilər"),
            ("delete_departmentworkingday", "Şöbənin tətil gününü silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.department} - {self.working_days_count} - {self.date}"


# ----------------------------------------------------------------------------------

class HoldingExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(HoldingWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingexceptionworker", "Mövcud holdinq istisna işçilərə baxa bilər"),
            ("add_holdingexceptionworker", "Holdinq istisna işçi əlavə edə bilər"),
            ("change_holdingexceptionworker", "Holdinq istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_holdingexceptionworker", "Holdinq istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"

class CompanyExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(CompanyWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_companyexceptionworker", "Mövcud şirkət istisna işçilərə baxa bilər"),
            ("add_companyexceptionworker", "Şirkət istisna işçi əlavə edə bilər"),
            ("change_companyexceptionworker", "Şirkət istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_companyexceptionworker", "Şirkət istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"

class OfficeExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(OfficeWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officeexceptionworker", "Mövcud ofis istisna işçilərə baxa bilər"),
            ("add_officeexceptionworker", "Office istisna işçi əlavə edə bilər"),
            ("change_officeexceptionworker", "Office istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_officeexceptionworker", "Office istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"

class DepartmentExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(DepartmentWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_departmentexceptionworker", "Mövcud şöbə istisna işçilərə baxa bilər"),
            ("add_departmentexceptionworker", "Şöbə istisna işçi əlavə edə bilər"),
            ("change_departmentexceptionworker", "Şöbə istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_departmentexceptionworker", "Şöbə istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"

class TeamExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(TeamWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_teamexceptionworker", "Mövcud team istisna işçilərə baxa bilər"),
            ("add_teamexceptionworker", "Team istisna işçi əlavə edə bilər"),
            ("change_teamexceptionworker", "Team istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_teamexceptionworker", "Team istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"

class PositionExceptionWorker(ExceptionWorker):
    working_day = models.ForeignKey(PositionWorkingDay, on_delete=models.CASCADE, related_name="exception_worker")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_positionexceptionworker", "Mövcud vəzifə istisna işçilərə baxa bilər"),
            ("add_positionexceptionworker", "Vəzifə istisna işçi əlavə edə bilər"),
            ("change_positionexceptionworker", "Vəzifə istisna işçi məlumatlarını yeniləyə bilər"),
            ("delete_positionexceptionworker", "Vəzifə istisna işçiməlumatalrını silə bilər")
        )

    def __str__(self) -> str:
        return f"{self.working_day} - {self.exception_workers} - {self.holidays}"
from django.contrib import admin

from holiday.models import (
    HoldingWorkingDay,
    EmployeeWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    DepartmentWorkingDay,
    PositionWorkingDay,
    HoldingExceptionWorker,
    TeamExceptionWorker,
    CompanyExceptionWorker,
    OfficeExceptionWorker,
    DepartmentExceptionWorker,
    PositionExceptionWorker
)

# Register your models here.
admin.site.register(HoldingWorkingDay)
admin.site.register(EmployeeWorkingDay)
admin.site.register(TeamWorkingDay)
admin.site.register(OfficeWorkingDay)
admin.site.register(CompanyWorkingDay)
admin.site.register(DepartmentWorkingDay)
admin.site.register(PositionWorkingDay)
admin.site.register(HoldingExceptionWorker)
admin.site.register(TeamExceptionWorker)
admin.site.register(CompanyExceptionWorker)
admin.site.register(DepartmentExceptionWorker)
admin.site.register(OfficeExceptionWorker)
admin.site.register(PositionExceptionWorker)



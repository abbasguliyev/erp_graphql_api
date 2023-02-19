from django.contrib import admin
from .models import (
    AdvancePayment, 
    Bonus, 
    CanvasserPrim, 
    DealerPrimNew, 
    SalaryDeduction, 
    SalaryView,
    VanLeaderPrimNew, 
    PaySalary, 
    CreditorPrim, 
    OfficeLeaderPrim
)
# Register your models here.

class SalaryViewAdmin(admin.ModelAdmin):
    search_fields = (
        "employee__id",
        "employee__fullname",
        
    )
    list_filter = [
        "employee__id",
        "date"
    ]

admin.site.register(AdvancePayment)
admin.site.register(Bonus)
admin.site.register(CanvasserPrim)
admin.site.register(DealerPrimNew)
admin.site.register(SalaryDeduction)
admin.site.register(SalaryView, SalaryViewAdmin)
admin.site.register(VanLeaderPrimNew)
admin.site.register(PaySalary)
admin.site.register(CreditorPrim)
admin.site.register(OfficeLeaderPrim)


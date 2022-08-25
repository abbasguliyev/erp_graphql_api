from django.contrib import admin
from .models import (
    HoldingCashboxIncome,
    HoldingCashboxExpense,
    OfficeKassaIncome,
    OfficeKassaExpense,
    CompanyCashboxIncome,
    CompanyCashboxExpense
) 
# Register your models here.
admin.site.register(HoldingCashboxIncome)
admin.site.register(HoldingCashboxExpense)
admin.site.register(OfficeKassaIncome)
admin.site.register(OfficeKassaExpense)
admin.site.register(CompanyCashboxIncome)
admin.site.register(CompanyCashboxExpense)

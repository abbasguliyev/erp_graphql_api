from django.contrib import admin
from account.models import (
    CutomerNote, 
    User, 
    Cutomer, 
    Region,
    EmployeeStatus
)
from django.contrib.auth.models import Permission

class RegionAdmin(admin.ModelAdmin):
    search_fields = (
        "region_name",
    )

# Register your models here.
admin.site.register(User)

admin.site.register(Cutomer)
admin.site.register(CutomerNote)

admin.site.register(Region, RegionAdmin)
admin.site.register(EmployeeStatus)

admin.site.register(Permission)
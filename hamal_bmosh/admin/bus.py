from django.contrib import admin
from nested_admin.nested import NestedStackedInline

from hamal_bmosh.models import Bus, HanichBusAssignment, BusStop


class HanichBusAssignmentInlineAdmin(NestedStackedInline):
    model = HanichBusAssignment
    fields = ["hanich", "bus"]
    extra = 0


class BusStopInlineAdmin(admin.TabularInline):
    model = BusStop
    fields = ["name", "arrival_time", "date"]
    extra = 0


class BusAdmin(admin.ModelAdmin):
    list_display = ("number", "direction", "company", "driver_name")
    inlines = [HanichBusAssignmentInlineAdmin, BusStopInlineAdmin]
    date_hierarchy = "date"
    fieldsets = (
        ("מספר וכיוון", {
            "fields": (("date", "number", "direction"),)
        }),
        ("פרטי אחראי נסיעה", {
            "fields": (("escort_name", "escort_phone"),)
        }),
        ("פרטי חברה ונהג", {
            "fields": (("company", "driver_name", "driver_phone"),)
        }),
    )
    search_fields = [
        "number",
        "escort_name",
        "escort_phone",
        "hanichbusassignment__hanich__first_name",
        "hanichbusassignment__hanich__last_name",
        "hanichbusassignment__hanich__personal_id",
        "hanichbusassignment__hanich__ken__ken_name",
        "hanichbusassignment__hanich__mahoz__mahoz_name",
    ]


class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "bus", "arrival_time", "date")
    list_filter = ("bus", "date")
    search_fields = ("name", "bus__number")
    date_hierarchy = "date"


admin.site.register(Bus, BusAdmin)
admin.site.register(BusStop, BusStopAdmin)

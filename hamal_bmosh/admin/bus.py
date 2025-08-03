from django.contrib import admin

from hamal_bmosh.models import Bus, HanichBusAssignment, BusStop


class HanichBusAssignmentInlineAdmin(admin.TabularInline):
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


class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "bus", "arrival_time", "date")
    list_filter = ("bus", "date")
    search_fields = ("name", "bus__number")
    date_hierarchy = "date"


admin.site.register(Bus, BusAdmin)
admin.site.register(BusStop, BusStopAdmin)

from django.contrib import admin

from hamal_bmosh.models import Mahoz, Ken


class Mahozadmin(admin.ModelAdmin):
    search_fields = ["mahoz_code", "mahoz_name"]
    list_display = ["mahoz_code", "mahoz_name"]
    readonly_fields = ["mahoz_code"]


class Kenadmin(admin.ModelAdmin):
    search_fields = ["ken_code", "ken_name", "mahoz__mahoz_name", "mahoz__mahoz_code"]
    list_display = ["ken_code", "ken_name", "mahoz__mahoz_name"]
    list_filter = ["mahoz"]


admin.site.register(Mahoz, Mahozadmin)
admin.site.register(Ken, Kenadmin)
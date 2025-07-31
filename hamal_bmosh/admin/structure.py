from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin

from hamal_bmosh.models import Mahoz, Ken, Grade


class MahozAdmin(admin.ModelAdmin):
    search_fields = ["mahoz_code", "mahoz_name"]
    list_display = ["mahoz_code", "mahoz_name"]
    readonly_fields = ["mahoz_code"]


class KenAdmin(admin.ModelAdmin):
    search_fields = ["ken_code", "ken_name", "mahoz__mahoz_name", "mahoz__mahoz_code"]
    list_display = ["ken_code", "ken_name", "get_mahoz_name"]
    readonly_fields = ["ken_code"]
    list_filter = [AutocompleteFilterFactory("מחוז", "mahoz")]
    autocomplete_fields = ["mahoz"]

    def get_mahoz_name(self, obj):
        return obj.mahoz.mahoz_name if obj.mahoz else None

    get_mahoz_name.short_description = "שם מחוז"


class GradeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Mahoz, MahozAdmin)
admin.site.register(Ken, KenAdmin)
admin.site.register(Grade, GradeAdmin)

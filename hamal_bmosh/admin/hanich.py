from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from hamal_bmosh.models import Hanich, StatusHanich
from hamal_bmosh.resources import HanichResource


class HanichAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = HanichResource
    search_fields = ["first_name", "last_name", "personal_id", "mahoz", "ken"]
    list_display = ["first_name", "last_name", "mahoz", "ken", "status_hanich"]
    autocomplete_fields = ["mahoz", "ken", "status_hanich"]
    list_filter = [AutocompleteFilterFactory("מחוז", "mahoz"),
                   AutocompleteFilterFactory("קן", "ken"),
                   AutocompleteFilterFactory("סטטוס", "status_hanich"),
                   "arrived_to_the_event"]

    fieldsets = (
        ("פרטים אישיים", {
            "fields": (
                "personal_id",
                "first_name",
                "last_name",
                "gender",
                "date_of_birth",
            )
        }), ("סטטוסים", {
            "fields": (
                "arrived_to_the_event",
                "status_hanich",
            )
        }
             ),

        ("פרטי קשר", {
            "fields": (
                "parent_name",
                "parent_phone",
                "second_parent_phone",
                "personal_phone",
                "email",
            )
        }),
        ("שיוך בתנועה", {
            "fields": (
                "mahoz",
                "ken",
                "grade",
            )
        }),
        ("העדפות והרשמה", {
            "fields": (
                "food_preference",
                "registration_date",
                "registration_time",
                "is_cancelled",
            )
        }),
    )


class StatusHanichAdmin(admin.ModelAdmin):
    list_display = ["status", "active_status"]
    search_fields = ["status"]


admin.site.register(Hanich, HanichAdmin)
admin.site.register(StatusHanich, StatusHanichAdmin)

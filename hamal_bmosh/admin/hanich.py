from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from hamal_bmosh.models import Hanich
from hamal_bmosh.resources import HanichResource


class HanichAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = HanichResource
    search_fields = ["first_name", "last_name", "personal_id", "mahoz", "ken"]
    list_display = ["first_name", "last_name", "mahoz", "ken"]
    autocomplete_fields = ["mahoz", "ken"]
    list_filter = [AutocompleteFilterFactory("מחוז", "mahoz"),
                   AutocompleteFilterFactory("קן", "ken")]

    fieldsets = (
        ("פרטים אישיים", {
            "fields": (
                "personal_id",
                "first_name",
                "last_name",
                "gender",
                "date_of_birth",
            )
        }),
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


admin.site.register(Hanich, HanichAdmin)

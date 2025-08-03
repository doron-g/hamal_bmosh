from admin_auto_filters.filters import AutocompleteFilterFactory
from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.shortcuts import redirect, render
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from hamal_bmosh.admin import HanichBusAssignmentInlineAdmin
from hamal_bmosh.models import Hanich, StatusHanich
from hamal_bmosh.resources import HanichResource


class HanichAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = HanichResource
    search_fields = ["first_name", "last_name", "personal_id", "mahoz__mahoz_name", "ken__ken_name"]
    list_display = ["first_name", "last_name", "mahoz", "ken", "status_hanich"]
    autocomplete_fields = ["mahoz", "ken", "status_hanich"]
    list_filter = [AutocompleteFilterFactory("מחוז", "mahoz"),
                   AutocompleteFilterFactory("קן", "ken"),
                   AutocompleteFilterFactory("סטטוס", "status_hanich"),
                   "arrived_to_the_event"]
    inlines = [HanichBusAssignmentInlineAdmin]
    actions = ["set_status_action"]

    fieldsets = (
        ("פרטים אישיים", {
            "fields": (
                ("first_name", "last_name"),
                ("personal_id", "gender", "date_of_birth"),
            )
        }), ("סטטוסים", {
            "fields": (
                ("arrived_to_the_event", "status_hanich", "is_cancelled"),
            )
        }
             ),

        ("פרטי קשר", {
            "fields": (
                ("parent_name", "parent_phone"),
                ("second_parent_phone", "personal_phone"),
                "email",
            )
        }),
        ("שיוך בתנועה", {
            "fields": (
                ("mahoz", "ken"),
                "grade",
            )
        }),
        ("העדפות והרשמה", {
            "fields": (
                "food_preference",
                ("registration_date", "registration_time"),

            )
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('set-status/', self.admin_site.admin_view(self.set_status_view), name='set_status_hanich'),
        ]
        return custom_urls + urls

    def set_status_action(self, request, queryset):
        if request.POST.get('select_across') == '1':
            # כל הרשומות במסנן הנוכחי
            all_ids = self.model.objects.filter(**request.GET.dict()).values_list('id', flat=True)
            ids = list(map(str, all_ids))
        else:
            # רק אלו שסומנו ב-V
            ids = request.POST.getlist(ACTION_CHECKBOX_NAME)

        return redirect(f'set-status/?ids={",".join(ids)}')

    set_status_action.short_description = "שנה סטטוס לחניכים נבחרים"

    def set_status_view(self, request):
        ids = request.GET.get("ids", "")
        hanich_ids = ids.split(",")

        if request.method == "POST":
            form = SetStatusForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data["status"]
                updated = Hanich.objects.filter(id__in=hanich_ids).update(status_hanich=status)
                self.message_user(request, f"הסטטוס עודכן ל־{status} עבור {updated} חניכים.")
                return redirect("..")
        else:
            form = SetStatusForm()

        return render(request, "admin/set_status.html", {
            "form": form,
            "ids": ids,
            "title": "שינוי סטטוס לחניכים נבחרים"
        })


class SetStatusForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=StatusHanich.objects.filter(active_status=True),
        label="בחר סטטוס חדש",
        required=True
    )


class StatusHanichAdmin(admin.ModelAdmin):
    list_display = ["status", "active_status"]
    search_fields = ["status"]


admin.site.register(Hanich, HanichAdmin)
admin.site.register(StatusHanich, StatusHanichAdmin)

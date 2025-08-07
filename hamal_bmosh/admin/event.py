from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from hamal_bmosh.models import Event, EventRosh, EventGroup, HanichInEvent


class EventAdmin(SimpleHistoryAdmin):
    list_display = ["event_name", "start_date", "end_date"]
    search_fields = ["event_name"]


class EventRoshAdmin(SimpleHistoryAdmin):
    list_display = ["rosh_name", "event"]
    search_fields = ["event__event_name", "rosh_name"]
    autocomplete_fields = ["event"]
    list_filter = [AutocompleteFilterFactory("אירוע", "event"), ]


class EventGroupAdmin(SimpleHistoryAdmin):
    list_display = ["group_name", "rosh", "rosh__event__event_name"]
    autocomplete_fields = ["rosh"]
    search_fields = ["group_name", "rosh__rosh_name", "rosh__event__event_name"]
    list_filter = [AutocompleteFilterFactory("ראש", "rosh"),
                   AutocompleteFilterFactory("אירוע", "rosh__event"),
                   ]


class HanichInEventAdmin(SimpleHistoryAdmin):
    list_display = ["hanich", "event", "group"]
    autocomplete_fields = ["hanich", "event", "group"]
    search_fields = ["hanich__name", "event__event_name"]
    list_filter = [AutocompleteFilterFactory("אירוע", "event"), ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventRosh, EventRoshAdmin)
admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(HanichInEvent, HanichInEventAdmin)

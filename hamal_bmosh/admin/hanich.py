from django.contrib import admin

from hamal_bmosh.models import Hanich


class Hanichadmin(admin.ModelAdmin):
    pass


admin.site.register(Hanich, Hanichadmin)

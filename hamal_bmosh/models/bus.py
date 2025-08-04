from django.db import models

import hebrew_constants


class BusDirection(models.TextChoices):
    TO = "הולך", "הלוך"
    FROM = "חוזר", "חזור"
    OTHER = "אחר", "אחר"


class Bus(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.DATE)
    number = models.CharField(max_length=20, verbose_name=hebrew_constants.BUS_NUMBER)
    direction = models.CharField(max_length=10, choices=BusDirection.choices, verbose_name=hebrew_constants.DIRECTION)
    company = models.CharField(max_length=100, verbose_name=hebrew_constants.COMPANY_NAME, null=True, blank=True)
    driver_name = models.CharField(max_length=100, verbose_name=hebrew_constants.DRIVER_NAME, null=True, blank=True)
    driver_phone = models.CharField(max_length=15, verbose_name=hebrew_constants.DRIVER_PHONE, null=True, blank=True)
    escort_name = models.CharField(max_length=100, verbose_name=hebrew_constants.ESCORT_NAME, null=True, blank=True)
    escort_phone = models.CharField(max_length=15, verbose_name=hebrew_constants.ESCORT_PHONE, null=True, blank=True)

    def __str__(self):
        return f"אוטובוס {self.number} ({self.get_direction_display()})"

    class Meta:
        verbose_name = hebrew_constants.BUS
        verbose_name_plural = hebrew_constants.BUSES


class BusStop(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.DATE)
    bus = models.ForeignKey(to="hamal_bmosh.Bus", on_delete=models.CASCADE, related_name="stops",
                            verbose_name=hebrew_constants.BUS)
    name = models.CharField(max_length=100, verbose_name=hebrew_constants.BUS_STOP_NAME)
    arrival_time = models.TimeField(verbose_name=hebrew_constants.ARRIVAL_TIME)

    class Meta:
        ordering = ['arrival_time']
        verbose_name = hebrew_constants.BUS_STOP
        verbose_name_plural = hebrew_constants.BUS_STOPS

    def __str__(self):
        return f"{self.name} ({self.arrival_time.strftime('%H:%M')})"


class HanichBusAssignment(models.Model):
    hanich = models.ForeignKey(to="hamal_bmosh.Hanich", on_delete=models.CASCADE, verbose_name=hebrew_constants.HANICH)
    bus = models.ForeignKey(to="hamal_bmosh.Bus", on_delete=models.CASCADE, verbose_name=hebrew_constants.BUS)
    note = models.TextField(null=True, blank=True, verbose_name=hebrew_constants.NOTE)

    class Meta:
        verbose_name = hebrew_constants.HANICH_BUS_ASSIGNMENT
        verbose_name_plural = hebrew_constants.HANICHIM_BUS_ASSIGNMENT

    def __str__(self):
        return f"{self.hanich} {self.bus}"

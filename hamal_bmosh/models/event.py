from django.db import models
from simple_history.models import HistoricalRecords

import hebrew_constants


class Event(models.Model):
    event_name = models.CharField(max_length=255, verbose_name=hebrew_constants.EVENT_NAME)
    start_date = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.START_DATE)
    end_date = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.END_DATE)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.event_name} ({self.start_date})"

    class Meta:
        verbose_name = hebrew_constants.EVENT
        verbose_name_plural = hebrew_constants.EVENTS
        constraints = [
            models.UniqueConstraint(
                fields=['event_name', 'start_date'],
                name='unique_event_name_start_date'
            )
        ]


class EventRosh(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rashim",
                              verbose_name=hebrew_constants.EVENT)
    rosh_name = models.CharField(max_length=100, verbose_name=hebrew_constants.ROSH_NAME)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.rosh_name} ({self.event.event_name})"

    class Meta:
        verbose_name = hebrew_constants.EVENT_ROSH
        verbose_name_plural = hebrew_constants.EVENTS_ROSH
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'rosh_name'],
                name='unique_event_rosh_name'
            )
        ]


class EventGroup(models.Model):
    rosh = models.ForeignKey(EventRosh, on_delete=models.CASCADE, related_name="groups",
                             verbose_name=hebrew_constants.EVENT_ROSH)
    group_name = models.CharField(max_length=100, verbose_name=hebrew_constants.GROUP_NAME)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.group_name} ({self.rosh.rosh_name})"

    class Meta:
        verbose_name = hebrew_constants.EVENT_GROUP
        verbose_name_plural = hebrew_constants.EVENT_GROUPS
        constraints = [
            models.UniqueConstraint(
                fields=['rosh', 'group_name'],
                name='unique_group_per_rosh'
            )
        ]


class HanichInEvent(models.Model):
    hanich = models.ForeignKey(to="hamal_bmosh.Hanich", on_delete=models.SET_NULL, related_name="event_participations",
                               null=True, verbose_name=hebrew_constants.HANICH)
    event = models.ForeignKey(to="hamal_bmosh.Event", on_delete=models.SET_NULL, related_name="hanichim", null=True,
                              verbose_name=hebrew_constants.EVENT)
    group = models.ForeignKey(to="hamal_bmosh.EventGroup", on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="hanichim", verbose_name=hebrew_constants.EVENT_GROUP)
    history = HistoricalRecords()

    def __str__(self):
        if self.hanich and self.event and self.group:
            return f"{self.hanich.first_name} {self.hanich.last_name} {self.event.event_name} {self.group.group_name}"
        return ""

    class Meta:
        verbose_name = hebrew_constants.HANICH_IN_EVENT
        verbose_name_plural = hebrew_constants.HANICHIM_IN_EVENTS
        constraints = [
            models.UniqueConstraint(fields=["hanich", "event"], name="unique_hanich_per_event")
        ]

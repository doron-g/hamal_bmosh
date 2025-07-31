from django.db import models
from simple_history.models import HistoricalRecords

import hebrew_constants
from hamal_bmosh.choices import GradeNameChoices


class Mahoz(models.Model):
    mahoz_code = models.CharField(null=False, blank=False, max_length=20, verbose_name=hebrew_constants.MAHOZ_CODE)
    mahoz_name = models.CharField(null=False, blank=False, max_length=100, verbose_name=hebrew_constants.MAHOZ_NAME)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mahoz_name}"

    class Meta:
        verbose_name = hebrew_constants.MAHOZ
        verbose_name_plural = hebrew_constants.MAHOZOT


class Ken(models.Model):
    ken_code = models.CharField(null=False, blank=False, max_length=20, verbose_name=hebrew_constants.KEN_CODE)
    ken_name = models.CharField(null=False, blank=False, max_length=100, verbose_name=hebrew_constants.KEN_NAME)
    mahoz = models.ForeignKey(to="Mahoz", on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=hebrew_constants.MAHOZ)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.ken_name} - {self.mahoz}"

    class Meta:
        verbose_name = hebrew_constants.KEN
        verbose_name_plural = hebrew_constants.KENIM


class Grade(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True, choices=GradeNameChoices.choices,
                            verbose_name=hebrew_constants.GRADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = hebrew_constants.GRADE
        verbose_name_plural = hebrew_constants.GRADES

from django.db import models
from simple_history.models import HistoricalRecords

import hebrew_constants
from hamal_bmosh.choices import Gender, FoodPreference


class Hanich(models.Model):
    personal_id = models.CharField(max_length=9, null=True, blank=True, unique=True,
                                   verbose_name=hebrew_constants.PERSONAL_ID)
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=hebrew_constants.FIRST_NAME)
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name=hebrew_constants.LAST_NAME)
    parent_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=hebrew_constants.PARENT_NAME)
    parent_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name=hebrew_constants.PARENT_PHONE)
    second_parent_phone = models.CharField(max_length=15, null=True, blank=True,
                                           verbose_name=hebrew_constants.SECOND_PARENT_PHONE)
    personal_phone = models.CharField(max_length=15, null=True, blank=True,
                                      verbose_name=hebrew_constants.PERSONAL_PHONE)
    email = models.EmailField(null=True, blank=True, verbose_name=hebrew_constants.EMAIL)
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True,
                              blank=True, verbose_name=hebrew_constants.GENDER)#FK
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.DATE_OF_BIRTH)
    mahoz = models.CharField(max_length=50, null=True, blank=True, verbose_name=hebrew_constants.MAHOZ)#FK
    ken = models.CharField(max_length=50, null=True, blank=True, verbose_name=hebrew_constants.KEN)#FK
    grade = models.CharField(null=True, blank=True, verbose_name=hebrew_constants.GRADE)
    food_preference = models.CharField(max_length=50, choices=FoodPreference.choices, null=True, blank=True,
                                       verbose_name=hebrew_constants.FOOD_PREFERENCE)
    registration_date = models.DateField(null=True, blank=True, verbose_name=hebrew_constants.REGISTRATION_DATE)
    registration_time = models.TimeField(null=True, blank=True, verbose_name=hebrew_constants.REGISTRATION_TIME)
    is_cancelled = models.BooleanField(default=False, verbose_name=hebrew_constants.IS_CANCELLED)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = hebrew_constants.HANICH
        verbose_name_plural = hebrew_constants.HANICHIM

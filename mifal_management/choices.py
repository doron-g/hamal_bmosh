from django.db import models


class Gender(models.TextChoices):
    MALE = 'male', 'זכר'
    FEMALE = 'female', 'נקבה'


class FoodPreference(models.TextChoices):
    MEAT = 'meat', 'בשרי/ת'
    MEAT_GLUTEN_FREE = 'meat_gluten_free', 'בשרי/ת ללא גלוטן'
    VEGAN = 'vegan', 'טבעוני/ת'
    VEGAN_GLUTEN_FREE = 'vegan_gluten_free', 'טבעוני/ת ללא גלוטן'
    VEGETARIAN = 'vegetarian', 'צמחוני/ת'
    VEGETARIAN_GLUTEN_FREE = 'vegetarian_gluten_free', 'צמחוני/ת ללא גלוטן'


class GradeNameChoices(models.TextChoices):
    FIRST = "א'", "א'"
    SECOND = "ב'", "ב'"
    THIRD = "ג'", "ג'"
    FOURTH = "ד'", "ד'"
    FIFTH = "ה'", "ה'"
    SIXTH = "ו'", "ו'"
    SEVENTH = "ז'", "ז'"
    EIGHTH = "ח'", "ח'"
    NINTH = "ט'", "ט'"
    TENTH = "י'", "י'"
    ELEVENTH = "י\"א", "י\"א"
    TWELFTH = "י\"ב", "י\"ב"
    THIRTEENTH = "י\"ג", "י\"ג"
    FOURTEENTH = "י\"ד", "י\"ד"
    ADULT = "מבוגרים", "מבוגרים"
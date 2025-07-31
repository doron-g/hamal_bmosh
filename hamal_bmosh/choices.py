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

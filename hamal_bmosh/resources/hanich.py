from import_export import resources, fields
from import_export.widgets import Widget

from hamal_bmosh.choices import Gender, FoodPreference
from hamal_bmosh.models import Hanich


class ChoicesWidget(Widget):
    def __init__(self, choices):
        self.choices = dict(choices)  # {'male': 'זכר', ...}
        self.reverse_choices = {v: k for k, v in self.choices.items()}  # {'זכר': 'male', ...}

    def clean(self, value, row=None, *args, **kwargs):
        return self.reverse_choices.get(value, None)

    def render(self, value, obj=None):
        return self.choices.get(value, '')


class HanichResource(resources.ModelResource):
    personal_id = fields.Field(column_name="ת.ז. חניך", attribute="personal_id")
    first_name = fields.Field(column_name="שם חניך", attribute="first_name")
    last_name = fields.Field(column_name="שם משפחה", attribute="last_name")
    parent_name = fields.Field(column_name="שם ההורה", attribute="parent_name")
    parent_phone = fields.Field(column_name="טלפון", attribute="parent_phone")
    second_parent_phone = fields.Field(column_name="טלפון שני", attribute="second_parent_phone")
    personal_phone = fields.Field(column_name="טלפון חניך",
                                  attribute="personal_phone")  # need to normalize all phone numbers
    email = fields.Field(column_name="כתובת מייל", attribute="email")
    gender = fields.Field(column_name="מין (ז / נ)", attribute="gender",
                          widget=ChoicesWidget(choices=Gender.choices))
    date_of_birth = fields.Field(column_name="תאריך לידה", attribute="date_of_birth")
    mahoz = fields.Field(column_name="מחוז", attribute="mahoz")
    ken = fields.Field(column_name="קן", attribute="ken")
    grade = fields.Field(column_name="שכבה", attribute="grade")
    food_preference = fields.Field(column_name="האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י",
                                   attribute="food_preference", widget=ChoicesWidget(choices=FoodPreference.choices))
    registration_date = fields.Field(column_name="ת. תשלום/שיחה", attribute="registration_date")
    registration_time = fields.Field(column_name="זמן תשלום/שיחה", attribute="registration_time")

    class Meta:
        model = Hanich
        import_id_fields = ["personal_id"]
        fields = [
            "personal_id",
            "first_name",
            "last_name",
            "parent_name",
            "parent_phone",
            "second_parent_phone",
            "personal_phone",
            "email",
            "gender",
            "date_of_birth",
            "mahoz",
            "ken",
            "grade",
            "food_preference",
            "registration_date",
            "registration_time"
        ]

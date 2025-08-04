from import_export import resources, fields
from import_export.widgets import Widget, ForeignKeyWidget

from hamal_bmosh.choices import Gender, FoodPreference
from hamal_bmosh.models import Hanich, Mahoz, Ken, Grade


class ChoicesWidget(Widget):
    def __init__(self, choices):
        self.choices = dict(choices)
        self.reverse_choices = {v: k for k, v in self.choices.items()}

    def clean(self, value, row=None, *args, **kwargs):
        return self.reverse_choices.get(value, None)

    def render(self, value, obj=None):
        return self.choices.get(value, '')


class KenWidgetWithMahozCreation(ForeignKeyWidget):
    def __init__(self, model, field='ken_name', *args, **kwargs):
        super().__init__(model, field=field, *args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None

        ken_name = value.strip()

        # מחפש קן קיים
        ken = Ken.objects.filter(ken_name=ken_name).first()
        if ken:
            return ken

        # אם לא קיים - ניצור מחוז אם צריך
        mahoz_name = row.get("מחוז", "").strip()
        if not mahoz_name:
            return None  # אין מחוז ואין קן - לא ניצור

        mahoz, _ = Mahoz.objects.get_or_create(mahoz_name=mahoz_name)

        # ניצור קן חדש
        ken = Ken.objects.create(ken_name=ken_name, mahoz=mahoz)
        return ken


class HanichResource(resources.ModelResource):
    personal_id = fields.Field(column_name="ת.ז. חניך", attribute="personal_id")
    first_name = fields.Field(column_name="שם חניך", attribute="first_name")
    last_name = fields.Field(column_name="שם משפחה", attribute="last_name")
    parent_name = fields.Field(column_name="שם ההורה", attribute="parent_name")
    parent_phone = fields.Field(column_name="טלפון", attribute="parent_phone")
    second_parent_phone = fields.Field(column_name="טלפון שני", attribute="second_parent_phone")
    personal_phone = fields.Field(column_name="טלפון חניך", attribute="personal_phone")
    email = fields.Field(column_name="כתובת מייל", attribute="email")
    gender = fields.Field(column_name="מין (ז / נ)", attribute="gender",
                          widget=ChoicesWidget(choices=Gender.choices))
    date_of_birth = fields.Field(column_name="תאריך לידה", attribute="date_of_birth")

    mahoz = fields.Field(
        column_name="מחוז",
        attribute="mahoz",
        widget=ForeignKeyWidget(model=Mahoz, field="mahoz_name")
    )

    ken = fields.Field(
        column_name="קן",
        attribute="ken",
        widget=KenWidgetWithMahozCreation(model=Ken)
    )

    grade = fields.Field(column_name="שכבה", attribute="grade", widget=ForeignKeyWidget(Grade, field="name"))

    food_preference = fields.Field(
        column_name="האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י",
        attribute="food_preference",
        widget=ChoicesWidget(choices=FoodPreference.choices)
    )

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

    def before_import_row(self, row, **kwargs):
        # ודא שהמחוז קיים לפני שהקן ייבדק
        mahoz_name = row.get("מחוז", "").strip()
        if mahoz_name:
            Mahoz.objects.get_or_create(mahoz_name=mahoz_name)

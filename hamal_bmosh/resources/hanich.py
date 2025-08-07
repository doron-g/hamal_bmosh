import re

from import_export import resources, fields
from import_export.widgets import Widget, ForeignKeyWidget, CharWidget

from hamal_bmosh.choices import Gender, FoodPreference
from hamal_bmosh.models import Hanich, Mahoz, Ken, Grade, HanichExtraQuestion


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

        ken = Ken.objects.create(ken_name=ken_name, mahoz=mahoz)
        return ken


class PhoneNumberWidget(CharWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return ""

        # הסרת כל מה שאינו ספרה
        digits = re.sub(r"\D", "", value)

        # טיפול במבנה של +972...
        if digits.startswith("972") and len(digits) > 9:
            digits = "0" + digits[3:]

        # חיתוך ל־10 תווים מקסימום (אם נותר משהו ארוך)
        if len(digits) > 10:
            digits = digits[:10]

        return digits


class HanichResource(resources.ModelResource):
    INCLUDED_COLUMNS = {
        "ת.ז. חניך",
        "שם חניך",
        "שם משפחה",
        "שם ההורה",
        "טלפון",
        "טלפון שני",
        "טלפון חניך",
        "כתובת מייל",
        "מין (ז / נ)",
        "תאריך לידה",
        "מחוז",
        "קן",
        "שכבה",
        "האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י",
        "ת. תשלום/שיחה",
        "זמן תשלום/שיחה",
    }
    EXCLUDED_COLUMNS = {
        "קוד אישור",
        "קוד קבוצה",
        "מנפיק קבלה",
        "מס' קבלה",
        "מס' ריכוז/הפקדה",
        "תאריך הפקדה",
        "סכום",
        "קבוצה",
        "חשבון הכנסות ראשי",
        "סכום לחשבון הכנסות ראשי",
        "חשבון הכנסות משני",
        "סיבסוד?",
        "הנחת אחים?",
        "בוטל?",
        "הוחזר חלקית?",
        "סכום החזר",
        "מזהה יחודי",
    }

    personal_id = fields.Field(column_name="ת.ז. חניך", attribute="personal_id")
    first_name = fields.Field(column_name="שם חניך", attribute="first_name")
    last_name = fields.Field(column_name="שם משפחה", attribute="last_name")
    parent_name = fields.Field(column_name="שם ההורה", attribute="parent_name")
    parent_phone = fields.Field(column_name="טלפון", attribute="parent_phone", widget=PhoneNumberWidget())
    second_parent_phone = fields.Field(column_name="טלפון שני", attribute="second_parent_phone",
                                       widget=PhoneNumberWidget())
    personal_phone = fields.Field(column_name="טלפון חניך", attribute="personal_phone", widget=PhoneNumberWidget())
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

    def after_import_row(self, row, row_result, **kwargs):
        instance = getattr(row_result, "instance", None)
        if not instance:
            return

        for column, value in row.items():
            if column in HanichResource.INCLUDED_COLUMNS or column in HanichResource.EXCLUDED_COLUMNS:
                continue

            if value is None or str(value).strip() == "":
                continue

            HanichExtraQuestion.objects.create(
                hanich=instance,
                question=column,
                answer=value,
            )

from django.urls import reverse
from rest_framework import status

from hamal_bmosh.models import Hanich, Mahoz, Event
from hamal_bmosh.models import HanichInEvent, HanichExtraQuestion
from hamal_bmosh.tests.base import HamalBaseTestCase, MinimalImportFormat


class HanichImportTestCase(HamalBaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = reverse("admin:hamal_bmosh_hanich_changelist")
        self.import_url = reverse("admin:hamal_bmosh_hanich_import")
        self.process_url = f"{self.base_url}process_import/"

    def test_import_single_hanich(self):
        response = self.client.get(self.import_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'form action=""')
        mock_data = [[
            ("ת.ז. חניך", "123456789"),
            ("שם חניך", "יוסי"),
            ("שם משפחה", "כהן"),
            ("שם ההורה", "אמא של יוסי"),
            ("טלפון", "0501234567"),
            ("טלפון שני", "0507654321"),
            ("טלפון חניך", "0509999999"),
            ("כתובת מייל", "yossi@example.com"),
            ("מין (ז / נ)", "ז"),
            ("תאריך לידה", "1985-01-01"),
            ("מחוז", "מחוז בדיקה"),
            ("קן", "קן בדיקה"),
            ("שכבה", "מבוגרים"),
            ("האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י", "צמחוני/ת"),
            ("ת. תשלום/שיחה", "2025-07-20"),
            ("זמן תשלום/שיחה", "18:51:46"),
        ]]
        upload_response = self.upload_to_import_form(mock_data)
        self.verify_response_after_upload_file(upload_response)

        process_response = self.upload_to_process_endpoint(upload_response)
        self.assertEqual(process_response.status_code, status.HTTP_200_OK)
        self.assertContains(
            process_response,
            "הייבוא הסתיים: נוספו 1, עודכנו 0, נמחקו 0, דולגו 0."
        )
        number_of_hanichim = Hanich.objects.count()
        self.assertEqual(number_of_hanichim, 1)

    def test_import_five_hanichim_from_different_kens_same_mahoz(self):
        base_row = [
            ("שם ההורה", "הורה של חניך"),
            ("טלפון", "0501234567"),
            ("טלפון שני", "0507654321"),
            ("טלפון חניך", "0509999999"),
            ("כתובת מייל", "test@example.com"),
            ("מין (ז / נ)", "ז"),
            ("תאריך לידה", "2010-01-01"),
            ("מחוז", "מחוז בדיקה"),
            ("שכבה", "י'"),
            ("האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י", "בשרי/ת"),
            ("ת. תשלום/שיחה", "2025-07-20"),
            ("זמן תשלום/שיחה", "10:00"),
        ]

        # מייצר 5 חניכים עם ת"ז, שם וקן שונים
        mock_data = []
        for i in range(5):
            row = base_row.copy()
            row.insert(0, ("ת.ז. חניך", f"12345678{i}"))
            row.insert(1, ("שם חניך", f"חניך{i}"))
            row.insert(2, ("שם משפחה", f"בדיקה{i}"))
            row.insert(10, ("קן", f"קן מספר {i}"))  # שדה קן במיקום הנכון
            mock_data.append(row)

        upload_response = self.upload_to_import_form(mock_data)
        self.verify_response_after_upload_file(upload_response)

        process_response = self.upload_to_process_endpoint(upload_response)
        self.assertEqual(process_response.status_code, status.HTTP_200_OK)
        self.assertContains(
            process_response,
            "הייבוא הסתיים: נוספו 5, עודכנו 0, נמחקו 0, דולגו 0."
        )
        self.assertEqual(Hanich.objects.count(), 5)

    def test_import_creates_mahoz_and_ken(self):
        # מוודא שאין מחוז קודם
        self.assertFalse(Mahoz.objects.filter(mahoz_name="מחוז חדש").exists())

        mock_data = [[
            ("ת.ז. חניך", "987654321"),
            ("שם חניך", "דני"),
            ("שם משפחה", "חדשה"),
            ("שם ההורה", "אמא של דני"),
            ("טלפון", "0501112222"),
            ("טלפון שני", "0503334444"),
            ("טלפון חניך", "0505556666"),
            ("כתובת מייל", "dani@example.com"),
            ("מין (ז / נ)", "ז"),
            ("תאריך לידה", "2009-05-10"),
            ("מחוז", "מחוז חדש"),
            ("קן", "קן חדש"),
            ("שכבה", "ח'"),
            ("האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י", "טבעוני/ת"),
            ("ת. תשלום/שיחה", "2025-07-25"),
            ("זמן תשלום/שיחה", "14:45"),
        ]]

        upload_response = self.upload_to_import_form(mock_data)
        self.verify_response_after_upload_file(upload_response)

        process_response = self.upload_to_process_endpoint(upload_response)
        self.assertEqual(process_response.status_code, status.HTTP_200_OK)
        self.assertContains(
            process_response,
            "הייבוא הסתיים: נוספו 1, עודכנו 0, נמחקו 0, דולגו 0."
        )

        # בדיקות על יצירת הנתונים
        self.assertEqual(Hanich.objects.count(), 1)
        self.assertTrue(Mahoz.objects.filter(mahoz_name="מחוז חדש").exists())
        self.assertTrue(Mahoz.objects.get(mahoz_name="מחוז חדש").ken_set.filter(ken_name="קן חדש").exists())

    from hamal_bmosh.models import Event, HanichInEvent, HanichExtraQuestion

    def test_import_single_hanich_with_extra_fields_and_ignored_fields(self):
        ignored_fields = {
            "קוד אישור", "קוד קבוצה", "מנפיק קבלה", "מס' קבלה", "מס' ריכוז/הפקדה", "תאריך הפקדה", "סכום",
            "קבוצה", "חשבון הכנסות ראשי", "סכום לחשבון הכנסות ראשי", "חשבון הכנסות משני",
            "סיבסוד?", "הנחת אחים?", "בוטל?", "הוחזר חלקית?", "סכום החזר", "מזהה יחודי",
        }

        included_fields = [
            ("שם חניך", "דנה"),
            ("שם משפחה", "כהן"),
            ("ת.ז. חניך", "123456789"),
            ("שם ההורה", "אמא של דנה"),
            ("טלפון", "0501234567"),
            ("טלפון שני", "0507654321"),
            ("טלפון חניך", "0509999999"),
            ("כתובת מייל", "dana@example.com"),
            ("מין (ז / נ)", "נ"),
            ("תאריך לידה", "2010-06-15"),
            ("מחוז", "מחוז הצפון"),
            ("קן", "קן כרמל"),
            ("שכבה", "ט'"),
            ("האם החניך/ה צמחוני/ת, בשרי/ת או טבעוני/ת?  פרט/י", "טבעוני/ת"),
            ("ת. תשלום/שיחה", "2025-07-20"),
            ("זמן תשלום/שיחה", "10:30"),
            ("שם אירוע", "מחנה קיץ תשפ\"ה"),
            ("תאריך אירוע", "2025-07-20"),
        ]

        extra_questions = [
            ("שומר שבת", "כן"),
            ("מידת חולצה?", "M"),
            ("תפקיד במחנה", "חניכה"),
        ]

        ignored_mock_fields = [(field, "ערך לבדיקה") for field in ignored_fields]

        mock_data = [[
            *included_fields,
            *extra_questions,
            *ignored_mock_fields
        ]]

        upload_response = self.upload_to_import_form(mock_data)
        self.verify_response_after_upload_file(upload_response)

        process_response = self.upload_to_process_endpoint(upload_response)
        self.assertEqual(process_response.status_code, 200)
        self.assertContains(
            process_response,
            "הייבוא הסתיים: נוספו 1, עודכנו 0, נמחקו 0, דולגו 0."
        )

        # נבדוק שנוצר החניך
        hanich = Hanich.objects.get(personal_id="123456789")
        self.assertEqual(hanich.first_name, "דנה")

        # נבדוק שנוצר האירוע
        event = Event.objects.get(event_name="מחנה קיץ תשפ\"ה", start_date="2025-07-20")
        self.assertIsNotNone(event)

        # נבדוק שנוצר HanichInEvent שמקשר בין החניך לאירוע
        h_in_event = HanichInEvent.objects.get(hanich=hanich, event=event)
        self.assertIsNotNone(h_in_event)

        # נבדוק שנשמרו רק השאלות הנוספות הרצויות
        answers = HanichExtraQuestion.objects.filter(hanich_in_event=h_in_event)
        self.assertEqual(answers.count(), len(extra_questions))
        for question, answer in extra_questions:
            self.assertTrue(answers.filter(question=question, answer=answer).exists())

        # נוודא ששדות להתעלמות לא נכנסו
        for ignored in ignored_fields:
            self.assertFalse(answers.filter(question=ignored).exists())

    def upload_to_import_form(self, mock_data):
        input_format = MinimalImportFormat.XLSX
        xlsx_file = self.create_in_memory_xlsx_file(mock_data)
        xlsx_file.seek(0)

        payload = {
            'format': input_format,
            'import_file': xlsx_file,
        }
        return self.client.post(self.import_url, payload)

    def verify_response_after_upload_file(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)
        self.assertFalse(response.context['result'].has_errors())
        self.assertIn('confirm_form', response.context)

    def upload_to_process_endpoint(self, upload_response):
        confirm_form = upload_response.context['confirm_form']
        confirmed_data = confirm_form.initial
        return self.client.post(self.process_url, confirmed_data, follow=True)

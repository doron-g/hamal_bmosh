from django.urls import reverse
from rest_framework import status

from hamal_bmosh.models import Hanich, Mahoz
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
        Mahoz.objects.create(mahoz_name="מחוז בדיקה")
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

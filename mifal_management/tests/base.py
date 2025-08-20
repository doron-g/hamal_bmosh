import io
from typing import List, Tuple

from django.contrib.auth import get_user_model
from import_export.formats.base_formats import XLSX
from openpyxl import Workbook
from rest_framework.test import APITestCase
from tablib import Dataset


class MinimalImportFormat:
    XLSX = "1"

class HamalBaseTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.super_user = self.given_super_user_exists()
        self.given_user_force_login(self.super_user)

    def given_super_user_exists(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(username="admin", password="admin1")
        return user

    def given_user_force_login(self, user):
        self.client.force_login(user=user)

    def generate_excel_file(self, headers, rows, filename="test.xlsx"):
        """
        מחזיר קובץ אקסל (BytesIO) שנוצר מזוג headers + rows.
        """
        dataset = Dataset()
        dataset.headers = headers
        for row in rows:
            dataset.append(row)

        xlsx_format = XLSX()
        xlsx_data = xlsx_format.export_data(dataset)
        file_obj = io.BytesIO(xlsx_data)
        file_obj.name = filename
        file_obj.seek(0)
        return file_obj

    def create_in_memory_xlsx_file(self,mock_data: List[List[Tuple]]) -> io.BytesIO:
        wb = Workbook()
        ws = wb.active
        headers = [item[0] for item in mock_data[0]]
        ws.append(headers)
        for row_data in mock_data:
            row = []
            for key, value in row_data:
                row.append(value)
            ws.append(row)

        memory_file = io.BytesIO()
        wb.save(memory_file)
        return memory_file





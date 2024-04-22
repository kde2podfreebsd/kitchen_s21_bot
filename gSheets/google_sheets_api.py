import datetime
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gCreds import kitchens21_creds
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsAPI:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(kitchens21_creds, self.scope)
        self.client = gspread.authorize(self.creds)

    def open_sheet(self, sheet_id: str = os.getenv("GOOGLE_SHEET_ID")):
        return self.client.open_by_key(sheet_id)

    def read_data(self, range_name, sheet_id: str = os.getenv("GOOGLE_SHEET_ID")):
        sheet = self.open_sheet(sheet_id)
        worksheet = sheet.sheet1
        return worksheet.get(range_name)

    def write_transaction(self, client_chat_id, client_username, amount, tx_date, sheet_id: str = os.getenv("GOOGLE_SHEET_ID")):
        sheet = self.open_sheet(sheet_id)
        worksheet = sheet.worksheet("Донатики")

        index = 2
        while True:
            if not worksheet.cell(index, 1).value:
                break
            index += 1

        worksheet.update(f'A{index}', [[client_chat_id, client_username, amount, tx_date.strftime('%d-%m-%Y %H:%M:%S')]])

    def write_feedback(self, client_chat_id, client_username, feedback, feed_date, sheet_id: str = os.getenv("GOOGLE_SHEET_ID")):
        sheet = self.open_sheet(sheet_id)
        worksheet = sheet.worksheet("Список пожеланий")

        index = 2
        while True:
            if not worksheet.cell(index, 1).value:
                break
            index += 1

        worksheet.update(f'A{index}', [[client_chat_id, client_username, feedback, feed_date.strftime('%d-%m-%Y %H:%M:%S')]])

    def write_total_recharge_amount_last_month(self, value, sheet_id: str = os.getenv("GOOGLE_SHEET_ID")):
        sheet = self.open_sheet(sheet_id)
        worksheet = sheet.worksheet("Донатики")
        worksheet.update('G3', [[value]])

    def write_total_recharge_amount(self, value, sheet_id: str = os.getenv("")):
        sheet = self.open_sheet(sheet_id)
        worksheet = sheet.worksheet("Донатики")
        worksheet.update('G2', [[value]])


if __name__ == "__main__":

    sheets_api = GoogleSheetsAPI()
    sheets_api.write_transaction(1234, "@donqhomo", 1000, datetime.date(2024, 4, 22))

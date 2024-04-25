import os.path
import requests
import datetime as dt
import pandas as pd
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"

def add_affmen_data_in_sheets(affmen_affise_data_list):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../token.json"):
        creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../creds.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    sheets = service.spreadsheets()

    row = 6
    for affmen in affmen_affise_data_list:
        sheets.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    body={
                                        "valueInputOption": "USER_ENTERED",
                                        "data": [
                                            {"range": f"Трекинг апрель!C{row}",
                                             "majorDimension": "ROWS",
                                             "values": [[affmen['Админ CPA-сети']]]},
                                            {"range": f"Трекинг апрель!D{row}",
                                             "majorDimension": "ROWS",
                                             "values": [[affmen['Даниил Lead-Magnet']]]},
                                            {"range": f"Трекинг апрель!E{row}",
                                             "majorDimension": "ROWS",
                                             "values": [[affmen['Никита Lead-Magnet']]]},
                                            {"range": f"Трекинг апрель!F{row}",
                                             "majorDimension": "ROWS",
                                             "values": [[affmen['Саппорт Лидмагнитов']]]},
                                        ]}).execute()

        sheets.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    body={
                                        "valueInputOption": "USER_ENTERED",
                                        "data": [
                                            {"range": f"Трекинг апрель!K{row}",
                                             "majorDimension": "ROWS",
                                             "values": [[affmen['Арбитражный Отдел']]]},
                                        ]}).execute()
        row = row + 2

        print(f'Добавили в таблицу данные за ', affmen['date'])
        time.sleep(1.5)


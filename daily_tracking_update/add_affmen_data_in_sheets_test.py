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
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "creds.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    sheets = service.spreadsheets()
    affmen_date_list = []
    affmen_1_charge_list = []
    affmen_2_charge_list = []
    affmen_3_charge_list = []
    affmen_4_charge_list = []
    affmen_5_charge_list = []

    for affmen in affmen_affise_data_list:
        affmen_date_list.append(affmen['date'])
        affmen_1_charge_list.append(affmen['Админ CPA-сети'])
        affmen_2_charge_list.append(affmen['Даниил Lead-Magnet'])
        affmen_3_charge_list.append(affmen['Никита Lead-Magnet'])
        affmen_4_charge_list.append(affmen['Саппорт Лидмагнитов'])
        affmen_5_charge_list.append(affmen['Арбитражный Отдел'])
        # sheets.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption='USER_ENTERED', range="Лист2!A2:F",
        #                        body={'values': [[str(affmen['date']),
        #                                          str(affmen['Админ CPA-сети']),
        #                                          str(affmen['Даниил Lead-Magnet']),
        #                                          str(affmen['Никита Lead-Magnet']),
        #                                          str(affmen['Саппорт Лидмагнитов']),
        #                                          str(affmen['Арбитражный Отдел'])]]}).execute()

    sheets.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "Лист2!A2:A",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_date_list]},
                {"range": "Лист2!B2:B",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_1_charge_list]},
                {"range": "Лист2!C2:C",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_2_charge_list]},
                {"range": "Лист2!D2:D",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_3_charge_list]},
                {"range": "Лист2!E2:E",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_4_charge_list]},
                {"range": "Лист2!F2:F",
                 "majorDimension": "COLUMNS",
                 "values": [affmen_5_charge_list]}
            ]}).execute()

    print(f'Добавили в таблицу')

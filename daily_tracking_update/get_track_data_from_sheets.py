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

def get_track_data_from_sheets(range):
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

    values = sheets.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=str(range),
        majorDimension='COLUMNS').execute()
    rows_date_coords = []
    start_coord = 6
    ignor_list = ['% ОТ ПЛАНА', 'ПРОГНОЗ', 'ВСЕГО', 'В ДЕНЬ']
    for cell in values['values'][0]:
        if cell not in ignor_list:
            rows_date_coords.append(f'C{start_coord}')
            start_coord = start_coord + 2
    return rows_date_coords

print(get_track_data_from_sheets('Трекинг январь!A6:A'))
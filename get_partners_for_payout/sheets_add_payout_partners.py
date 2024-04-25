import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from affise_get_payout_partners import affise_get_payout_partners

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"

def sheets_add_payout_partners():
    creds = None
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

    for partner in affise_get_payout_partners():
        print(f"Пробуем добавить партнера {partner['partner_id']} в гугл таблицу")
        work_sheet_name = 'балансы выплаты!'
        cell_range_insert = 'A1'
        values = [
            [partner['create_date'], partner['partner_id'], partner['partner_ref_id'],
             partner['balance'], partner['earning_this_week'], partner['payout']]
        ]
        value_range_body = {
            "majorDimension": "ROWS",
            "values": values
        }

        service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption="USER_ENTERED",
            range=work_sheet_name + cell_range_insert,
            body=value_range_body
        ).execute()

        print(f"Успешно вставили данные новорега {partner['partner_id']} в гугл таблицу. Спим 1 секунду и идем дальше")
        time.sleep(1)

sheets_add_payout_partners()

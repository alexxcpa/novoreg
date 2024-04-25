import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from database import db
from novoreg_table.logs import logger as log

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"

def sheets_add_new_partners():
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

    for partner in db.get_partners_for_sheets():
        if partner['status'] == 'no_chat':
            status = 'Нет общения'
        else:
            status = 'Есть общение'
        if partner['target'] == 'True':
            target = 'Да'
        else:
            target = 'Нет'
        if partner['send_hello'] == 'True':
            send_hello = 'Да'
        else:
            send_hello = 'Нет'
        if partner['tg_send_hello_error'] is None:
            tg_send_hello_error = ""
        else:
            tg_send_hello_error = partner['tg_send_hello_error']

        log.msg.info(f"Пробуем добавить партнера {partner['id']} в гугл таблицу")
        work_sheet_name = 'тикеты!'
        cell_range_insert = 'A1'
        values = [
            [status, partner['id'], target, partner['created_at'], "", partner['ref_partner'],
             partner['email'], "", "", "", partner['telegram'], "", "", tg_send_hello_error, send_hello,
             "", "", "", "", "", "", "", "", "", partner['experience'], "", partner['sources'], partner['verticals'],
             "", "", "", "", "", "", "", "", "", "", partner['about_us']]
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

        log.msg.info(f"Успешно вставили данные новорега {partner['id']} в гугл таблицу. Спим 1 секунду и идем дальше")
        db.add_google_sheets_status(partner['id'])
        time.sleep(1)

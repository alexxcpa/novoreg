import sqlite3
import requests

import db

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1w1-CZuuYjFFVyVM50I_eBernqm8hKi2iu2WmgJM4xLI"


def update_google_creds():
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

    return service


def get_partners_for_update():
    with open('partners.txt', 'r') as file:
        partners_form_check_list = []
        for i in file:
            partners_form_check_list.append(i.strip('\n'))
        return partners_form_check_list


def sheets_get_form_partners():
    service = update_google_creds()

    values = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range='Ответы на форму!A2:J',
        majorDimension='ROWS'
    ).execute()
    form_partners_info_list = []
    for partner in values['values']:
        form_partner_info = {'form_date': partner[0], 'name': partner[1], 'partner_id': partner[2],
                             'experience': partner[3], 'verticals': partner[4], 'sources': partner[5],
                             'experience_years': partner[6], 'segment': partner[7], 'solo_or_team': partner[8],
                             'about_us': partner[9]}
        form_partners_info_list.append(form_partner_info)
    # for i in form_partners_info_list:
    #     print(i)
    return form_partners_info_list


def sheets_add_update_partners(partners_info_list):
    service = update_google_creds()

    for partner in partners_info_list:
        if partner['status'] == 'no_chat':
            status = 'Нет общения'
        elif partner['status'] == 'delete_chat':
            status = 'Удалил чат'
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
        if partner['name'] is not None:
            name = partner['name']
        else:
            name = ""
        if partner['hello_answer'] is not None:
            hello_answer = 'Да'
        else:
            hello_answer = ""
        if partner['segment'] is not None:
            segment = partner['segment']
        else:
            segment = ""
        if partner['form'] == 'True':
            form = "Да"
        else:
            form = ""
        if partner['experience'] is not None:
            experience = partner['experience']
        else:
            experience = ""
        if partner['experience_years'] is not None:
            experience_years = partner['experience_years']
        else:
            experience_years = ""
        if partner['sources'] is not None:
            sources = partner['sources']
        else:
            sources = ""
        if partner['verticals'] is not None:
            verticals = partner['verticals']
        else:
            verticals = ""
        if partner['solo_or_team'] is not None:
            solo_or_team = partner['solo_or_team']
        else:
            solo_or_team = ""
        if partner['connect_offers'] == 'True':
            connect_offers = "Да"
        else:
            connect_offers = ""

        print(f"Пробуем добавить партнера {partner['partner_id']} в гугл таблицу")
        work_sheet_name = 'обновление статусов!'
        cell_range_insert = 'A2'
        values = [
            [status, partner['partner_id'], target, partner['created_at'], name, partner['ref_partner'],
            partner['email'], "", "", "", partner['telegram'], "", "", "", send_hello, hello_answer,
            "", "", "", "", "", segment, form, "", experience, experience_years, sources,
            verticals, solo_or_team, "", "", connect_offers, "", "", "", "", "", "", partner['about_us']]
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
        print(f"Успешно добавили партнера {partner['partner_id']} в гугл таблицу")
        time.sleep(2)

def main():
    print('Пробуем получить партнеров с листа Ответ на форму')
    sheets_partners_info_form_list = sheets_get_form_partners()
    print('Успешно получили партнеров с листа Ответ на форму')
    partners_id_list = get_partners_for_update()
    partners_id_update_status_list = []
    for partners in sheets_partners_info_form_list:
        partners_id_update_status_list.append(partners['partner_id'])

    for partner_id in partners_id_list:
        if partner_id in partners_id_update_status_list:
            for partner_info in sheets_partners_info_form_list:
                db.update_partner_status(partner_info)
    print('Успешно обновили статусы в базе')

    update_partner_info_for_sheets = []
    for partner_id in partners_id_list:
        partner_info = db.get_update_partner_for_sheets(partner_id)
        update_partner_info_for_sheets.append(partner_info)

    sheets_add_update_partners(update_partner_info_for_sheets)



if __name__ == '__main__':
    main()
    # sheets_get_form_partners()

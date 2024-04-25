import requests
import time
import datetime as dt

from database import db
from novoreg_table.logs import logger as log

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'


def affise_get_new_partners():
    today = str(dt.date.today())
    yesterday = str(dt.date.today() - dt.timedelta(days=1))
    try:
        url = f'https://api-lead-magnet.affise.com/3.0/admin/partners?limit=500&page=61&status=active'
        headers = {'API-Key': AFFISE_API_KEY}
        r = requests.get(url, headers=headers)
        res = r.json()
        # print("Запросили новорегов в аффайз ")
        log.msg.info("Запросили новорегов в аффайз")
        if res['status'] == 1:
            log.msg.info("Успешно получили новорегов в аффайз")
        time.sleep(0.1)
        partners_list = []
        for partner in res['partners']:
            if today in partner['created_at'] or yesterday in partner['created_at']:
                partners_list.append(partner)
        partners_info_list = []
        for partner in partners_list:
            create_date, create_time = str(partner['created_at']).split(" ")
            partner_info = {'created_at': create_date, 'email': partner['email'], 'id': partner['id']}
            if partner['ref'] is not None:
                partner_info['ref_id'] = partner['ref']
            for field in partner['customFields']:
                if field['id'] == 1:
                    if "https://t.me/" in field['value']:
                        partner_info['telegram'] = field['value']

                    elif "https://t.me/" not in field['value']:
                        try:
                            partner_info['telegram'] = int(field['value'])
                        except ValueError:
                            tg_value = "https://t.me/" + str(field['value']).strip('@')
                            partner_info['telegram'] = tg_value
                elif field['id'] == 5:
                    partner_info['phone'] = field['value']
                elif field['id'] == 6:
                    partner_info['another_contacts'] = field['value']
                elif field['id'] == 7:
                    partner_info['experience'] = field['value']
                elif field['id'] == 8:
                    partner_info['verticals'] = field['value']
                elif field['id'] == 9:
                    partner_info['sources'] = field['value']
                elif field['id'] == 10:
                    partner_info['about_us'] = field['value']
            partners_info_list.append(partner_info)

        db_partners = db.get_partners_id()

        for partner in partners_info_list:
            if partner['id'] not in db_partners:
                if db.add_new_partner(partner):
                    log.msg.info(f"Успешно добавили партнера {partner['id']} в базу")
        return True

    except Exception as err:
        log.msg.error('Ошибка. Не смогли добавить новых пользователей в таблицу', err)


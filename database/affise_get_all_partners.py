import requests
import time
import datetime as dt

from database import db

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'


def affise_get_all_partners():
    for page in range(1, 61): # с 58 по 61 на 58 ошибка

        url = f'https://api-lead-magnet.affise.com/3.0/admin/partners?limit=500&page={page}&status=active'
        headers = {'API-Key': AFFISE_API_KEY}
        r = requests.get(url, headers=headers)
        res = r.json()
        print("Запросили новорегов в аффайз ")
        if res['status'] == 1:
            print(f"Успешно получили новорегов в аффайз на страницe {page}")
        time.sleep(0.1)
        partners_list = []
        for partner in res['partners']:
                partners_list.append(partner)
        partners_info_list = []
        for partner in partners_list:
            if 'fakepartner' in partner['email']:
                continue
            else:
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

        for partner_info in partners_info_list:
            db.add_new_partner(partner_info)
            # print(partner_info)
        print('Успешно добавили партнеров в базу')


affise_get_all_partners()






        # db_partners = db.get_partners_id()
        #
        # for partner in partners_info_list:
        #     if partner['id'] not in db_partners:
        #         if db.add_new_partner(partner):
        #             print(f"Успешно добавили партнера {partner['id']} в базу")
        # # for partner in partners_info_list:
        # #     print(partner)
        # return True




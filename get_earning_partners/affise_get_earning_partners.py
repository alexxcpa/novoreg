import requests
import time
import datetime

# from partners import partners_list_22, partners_list_23


AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'

partners_list_22 = []
partners_list_23 = []

def affise_get_earning_partners():
    for page in range(1, 60):
        try:
            url = f'https://api-lead-magnet.affise.com/3.0/admin/partners?limit=500&page={page}'
            headers = {'API-Key': AFFISE_API_KEY}
            r = requests.get(url, headers=headers)
            res = r.json()
            print("Запросили в аффайз вебов на страничке ", page)
            for partner in res['partners']:
                create_date, create_time = str(partner['created_at']).split(' ')
                update_date, update_time = str(partner['updated_at']).split(' ')
                if '2022' in create_date:
                    ref_info = {'create_date': create_date, 'partner': partner['id'], 'ref_partner': partner['ref']}
                    partners_list_22.append(ref_info)
                elif '2023' in create_date:
                    ref_info = {'date': create_date, 'partner': partner['id'], 'ref_partner': partner['ref']}
                    partners_list_23.append(ref_info)
            time.sleep(0.1)
        except Exception as err:
            print('Ошибка', err)

    # print(partners_list_22)
    # print(len(partners_list_22))
    # print("----------------")
    # print(partners_list_23)
    # print(len(partners_list_23))

    for partner in partners_list_22:
        url = f"https://api-lead-magnet.affise.com/3.0/stats/getbypartner?filter[date_from]={partner['create_date']}&filter[date_to]=2022-12-31&filter[partner]={partner['partner']}&orderType=asc&locale=en&limit=1"
        headers = {'API-Key': AFFISE_API_KEY}
        r = requests.get(url, headers=headers)
        res = r.json()
        # print("Запросили в аффайз статистику по вебу ", partner['partner'])
        if len(res['stats']) == 0:
            # print('Не смогли получить статистку по вебу', partner['partner'])
            continue
        print(partner['create_date'], res['stats'][0]['slice']['affiliate']['id'], partner['ref_partner'], res['stats'][0]['actions']['confirmed']['earning'])

affise_get_earning_partners()
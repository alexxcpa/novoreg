import requests
import time
import datetime

# from partners import partners_list_22, partners_list_23


AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'

manager = '5fcf594293079980c967281a'

DATE_FROM = "2024-04-22"
DATE_TO = "2024-04-28"

def affise_get_earning_by_partner(date_from, date_to, partner_id):
    url = f"https://api-lead-magnet.affise.com/3.0/stats/getbypartner?filter[date_from]={date_from}&filter[date_to]={date_to}&filter[partner]={partner_id}&orderType=asc&locale=en&limit=1"
    headers = {'API-Key': AFFISE_API_KEY}
    r = requests.get(url, headers=headers)
    res = r.json()
    if len(res['stats']) == 0:
        print('Не смогли получить статистку за неделю по партнеру', partner_id)
        return None
    earning = res['stats'][0]['actions']['confirmed']['earning']
    return earning

def affise_get_payout_partners():
    partners_info_list = []
    for page in range(1, 6):
        try:
            print(f'Запрос партнеров с балансом на странице {page}')
            url = f'https://api-lead-magnet.affise.com/3.0/admin/partners?limit=500&page={page}&status=active&with_balance=1'
            headers = {'API-Key': AFFISE_API_KEY}
            r = requests.get(url, headers=headers)
            res = r.json()
            if res['status'] == 1 and len(res['partners']) > 0:
                print(f'Успешно получили партнеров с балансом на странице {page}')
                for partner in res['partners']:
                    try:
                        if partner['manager'] is None or manager in partner['manager']['id']:
                            if partner['balance']['RUB']['balance'] >= 5000:
                                create_date, create_time = str(partner['created_at']).split(' ')
                                # print(partner['id'], partner['manager']['id'])
                                partner_info = {"create_date": create_date, "partner_id": partner['id'], "partner_ref_id": partner['ref'], "balance": partner['balance']['RUB']['balance']}
                                partners_info_list.append(partner_info)
                            else:
                                continue
                    except Exception as partner_err:
                        print(f"Партнер {partner}: Не смогли получить. {type(partner['manager'])} {partner_err}")
            else:
                print(f'Не смогли получить партнеров с балансом на странице {page}')
        except Exception as err:
            print('Ошибка', err)

    for partner in partners_info_list:
        earning_this_week = affise_get_earning_by_partner(DATE_FROM, DATE_TO, partner['partner_id'])
        if earning_this_week is not None:
            partner['earning_this_week'] = earning_this_week
            partner['payout'] = partner['balance'] - earning_this_week
        else:
            partner['earning_this_week'] = 0
            partner['payout'] = partner['balance']
    # for partner in partners_info_list:
    #     print(partner)
    # print(len(partners_info_list))
    return partners_info_list

# affise_get_payout_partners()
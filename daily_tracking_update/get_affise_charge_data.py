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

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'


def get_affise_charge_data():
    start_date = dt.datetime(2024, 4, 1)
    end_date = dt.datetime(2024, 4, 30)
    # start_date = dt.datetime(2023, 11, 27)
    # end_date = dt.datetime(2023, 12, 31)

    date_range = pd.date_range(min(start_date, end_date),
                               max(start_date, end_date)).strftime('%Y-%m-%d').tolist()
    affman_list = ['Админ CPA-сети',
                   'Даниил Lead-Magnet',
                   'Никита Lead-Magnet',
                   'Саппорт Лидмагнитов',
                   'Арбитражный Отдел']

    affman_affise_data_list = []
    for date in date_range:
        affman_affise_data = {}
        try:
            url = f'https://api-lead-magnet.affise.com/3.0/stats/getbyaffiliatemanager?filter[date_from]={date}&filter[date_to]={date}&orderType=asc'
            headers = {'API-Key': AFFISE_API_KEY}
            print(f"Запрос в аффайз за период {date}")
            r = requests.get(url, headers=headers)
            res = r.json()
            if len(res['stats']) != 0:
                valid_date = str(date).split('-')
                affman_affise_data['date'] = f'{valid_date[2]}.{valid_date[1]}'
                for i in res['stats']:
                    if str(i['slice']['affiliate_manager_id']['title']) in affman_list:
                        affman_affise_data[str(i['slice']['affiliate_manager_id']['title'])] = i['actions']['confirmed']['charge']
                        print(f'Добавили данные за {date}')
                print('Получили результат', affman_affise_data)
                time.sleep(0.2)
                affman_affise_data_list.append(affman_affise_data)
            else:
                print('Не смогли получить разультат за', date)
                break

        except Exception as err:
            print('Ошибка', err)

    return affman_affise_data_list

#
# print(len(get_affise_charge_data()))
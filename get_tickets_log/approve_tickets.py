import requests
import time

import logger as log

from database import db

from tg_methods import send_message_tg

AFFISE_API_KEY = '1472b075254d6df44e295b3912665295'
OFFER_BLACK_LIST = [686, 1486, 848, 1299, 1370, 1421, 1527, 1586, 1553, 1460]

FROD_MSG = """
 🚯Обращаю внимание, что у нас проводится глубокая проверка на фрод и мотивированный трафик. Надеюсь на понимание и плодотворное сотрудничество😉
 """

ABOUT_LIMIT = """
[Подробнее про лимит в 100 конверсий](https://docs.google.com/document/d/1FqOnKFEzHI7SvmyVSloW78ehxLy6MctDqFpminFCUHo/edit?usp=sharing)
"""

def tg_send_info(ticket, good_connect_offers_list, frod_msg: bool):
    msg_title = f"Партнеру {ticket['partner']} подключили офферы:"
    if frod_msg is True:
        frod_msg = FROD_MSG
    else:
        frod_msg = ""
    offers_msg = msg_title + '\n \n👉' + '\n \n👉'.join(good_connect_offers_list) + '\n \n' + 'На каждый оффер стартовый лимит 100 конверсий' + '\n' + frod_msg + '\n' + ABOUT_LIMIT
    send_message_tg(offers_msg)

def approve_tickets(ticket_list):
    if ticket_list is None:
        log.msg.info(f'Нет доступных тикетов')
        return None
    try:
        for ticket in ticket_list:
            time.sleep(1)
            log.msg.info(f"Партнер {ticket['partner']} Пробуем подключить офферы")
            good_connect_offers_list = []
            if len(ticket['offers_list']) > 10:
                log.msg.info(f"Слишком большое количество офферов за раз. Пропускаем веба {ticket['partner']}")
                continue
            for offer in ticket['offers_list']:
                if offer['offer_id'] in OFFER_BLACK_LIST:
                    log.msg.info(f"Партнер {ticket['partner']} : Тикет {offer['ticket_id']} : Оффер {offer['offer_id']} на данный момент находится в блек листе")
                    continue
                log.msg.info(f"Партнер {ticket['partner']}: Пробуем подключить оффер {offer['offer_id']} в тикете {offer['ticket_id']}" )
                params = {'do': 'approve'}
                url = f"https://api-lead-magnet.affise.com/3.0/admin/ticket/{offer['ticket_id']}/offer"
                headers = {'API-Key': AFFISE_API_KEY}
                r = requests.post(url, headers=headers, data=params)
                res = r.json()
                if res['status'] == 1:
                    good_connect_offers_list.append(f"[{offer['offer_title'].replace('[', '(').replace(']', ')')}](https://lead-magnet.affise.com/v2/offer/{offer['offer_id']}/general)")
                    log.msg.info(f"Партнер {ticket['partner']}: Успешно подключили оффер {offer['offer_id']}")

            # log.msg.info(f"Пробуем запросить статус подлкючения офферов у партнера {ticket['partner']}")

            db_partners_list = db.get_partners_id()
            if len(good_connect_offers_list) > 0:
                if ticket['partner'] in db_partners_list:
                    novoreg_status = db.get_novoreg_status(ticket['partner'], 'connect_offers')
                    if novoreg_status is None:
                        db.set_novoreg_status(ticket['partner'], 'connect_offers', 'True')
                        tg_send_info(ticket, good_connect_offers_list, frod_msg=True)
                    else:
                        tg_send_info(ticket, good_connect_offers_list, frod_msg=False)
                else:
                    tg_send_info(ticket, good_connect_offers_list, frod_msg=False)

    except Exception as err:
        log.msg.error(f'Получили ошибку: {err}')

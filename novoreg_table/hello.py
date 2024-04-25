from tg_auth_acc_1 import tg_auth_acc_1 as tg_1
from tg_auth_acc_2 import tg_auth_acc_2 as tg_2
from database import db
import random
import time
from messages import acc_1_msg_tuple, acc_2_msg_tuple


def hello_sendler():
    for partner in db.get_partners_for_hello():
        acc1_message = random.choice(acc_1_msg_tuple)
        tg_1_res = tg_1.hello_sendler_acc_1(partner['telegram'], partner['id'], acc1_message)
        if tg_1_res is True:
            db.add_good_hello_status(partner['id'])
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'])
            time.sleep(10)
            continue
        if tg_1_res == "[400 USERNAME_INVALID]" or tg_1_res == "[400 USERNAME_NOT_OCCUPIED]":
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'])
            db.add_bad_hello_status("Невалидный тг", partner['id'])
            continue
        if tg_1_res is False:
            db.add_bad_hello_status("Не смогли отправить привет в тг", partner['id'])
            continue
        if tg_1_res == "[400 PEER_FLOOD]":
            tg_1.add_to_contact_acc_1(partner['telegram'], partner['id'])
            acc2_message = random.choice(acc_2_msg_tuple)
            tg_2_res = tg_2.hello_sendler_acc_2(partner['telegram'], partner['id'], acc2_message)
            if tg_2_res is True:
                db.add_good_hello_status(partner['id'])
                tg_2.add_to_contact_acc_2(partner['telegram'], partner['id'])
                time.sleep(10)
                continue
            if tg_2_res is False:
               db.add_bad_hello_status("Не смогли отправить привет в тг", partner['id'])
               continue
            if tg_2_res == "[400 USERNAME_NOT_OCCUPIED]" or tg_2_res == "[400 USERNAME_INVALID]":
                db.add_bad_hello_status("Невалидный тг", partner['id'])
                continue
            if tg_2_res == "[400 PEER_FLOOD]":
                print('Не смогли отправить приветы с обоих аккаунтов. Бан на обоих')
                break









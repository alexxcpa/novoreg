from pyrogram import Client

# user api data for support tg_account
API_ID_ACC_1 = 23290491
API_HASH_ACC_1 = '50178fc36db4006742b7fbe2f44bae5d'

TG_BOT_TOKEN = '6444085476:AAESgETTwFsi_HPRuXzUpxok6AqXAPFXg0s'
CHAT_ID = '1457459092'

test_user = "Alexey_Patunin_LM"
test_user_2 = "investor"
test_user_id = "32703"
message = "Привет"

def hello_sendler_acc_1(partner_user_name, partner_id, message):
    try:
        with Client('account') as app:
            app.send_message(partner_user_name, message)
            print(f"Аккаунт 1 :: Партнер {partner_id} :: Успешно отправили привет партнеру. Спим 30 сек.")
        return True
    except Exception as err:
        if "[400 PEER_FLOOD]" in str(err):
            # print(err, type(err))
            print(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Аккаунт временно в бане.')
            return "[400 PEER_FLOOD]"
        elif "[400 USERNAME_INVALID]" in str(err):
            # print(err, type(err))
            print(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            # print(err, type(err))
            print(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли отправить привет. Пользователь с именем {partner_user_name} не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        print(err)
        return False

def add_to_contact_acc_1(partner_user_name, partner_id):
    try:
        with Client('account') as app:
            app.add_contact(partner_user_name, first_name=str(partner_id))
            print(f"Аккаунт 1: Успешно добавили в контакты партнера {partner_id}.")
            return True
    except Exception as err:
        if "[400 USERNAME_INVALID]" in str(err):
            print(f'Аккаунт 1: Не смогли добавить в контакты  {partner_id}: Некорректно введено имя пользователя')
            return "[400 USERNAME_INVALID]"
        elif "[400 USERNAME_NOT_OCCUPIED]" in str(err):
            # print(err, type(err))
            print(f'Аккаунт 1 :: Партнер {partner_id} :: Не смогли добавить в контакты. Пользователь не найден')
            return "[400 USERNAME_NOT_OCCUPIED]"
        print(err)
        return False

# hello_sendler_acc_1(test_user_2, test_user_id, message)

        cur.execute(f"""INSERT INTO novoreg (status, partner_id, target, created_at, name, ref_partner, email, phone,
vk, skype, telegram, country, alter_send_hello, tg_send_hello_error, send_hello, hello_answer, second_hello, third_hello,
read_no_answer, no_read, second_hello_answer, segment, form, answers, experience, experience_years, sources, verticals,
solo_or_team, educational, top_offers, connect_offers, first_traffic, first_payment, froder, feedback_push, get_feedback,
stop_traffic_reason, about_us)        
                                      VALUES (''{partner['status']}', '{partner['partner_id']}', '{partner['target']}',
'{partner['created_at']}', '{partner['name']}', '{partner['ref_partner']}', '{partner['email']}', '{partner['phone']}', 
'{partner['vk']}', '{partner['skype']}', '{partner['telegram']}', '{partner['country']}', '{partner['alter_send_hello']}',
'{partner['tg_send_hello_error']}', '{partner['send_hello']}', '{partner['hello_answer']}', '{partner['second_hello']}'
'{partner['third_hello']}', '{partner['read_no_answer']}', '{partner['no_read']}', '{partner['second_hello_answer']}',
'{partner['segment']}', '{partner['form']}', '{partner['answers']}', '{partner['experience']}', '{partner['experience_years']}',
'{partner['sources']}', '{partner['verticals']}', '{partner['solo_or_team']}', '{partner['educational']}',
'{partner['top_offers']}', '{partner['connect_offers']}', '{partner['first_traffic']}', '{partner['first_payment']}',
'{partner['froder']}', '{partner['feedback_push']}', '{partner['get_feedback']}', '{partner['stop_traffic_reason']}',
'{partner['about_us']}')""")
        db.commit()
        db.close()

import sqlite3


def add_new_table():
    db = sqlite3.connect('../database/../database/novoreg.db')

    cur = db.cursor()

    cur.execute(""" CREATE TABLE novoreg_main (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status text,
    partner_id integer,
    target text,
    created_at date,
    name text,
    ref_partner integer,
    email text,
    phone integer,
    vk text,
    skype text,
    telegram text,
    country text,
    alter_send_hello text,
    tg_send_hello_error text,
    send_hello text,
    hello_answer text,
    second_hello text,
    third_hello text,
    read_no_answer text,
    no_read text,
    second_hello_answer text,
    segment text,
    form text,
    answers text,
    experience text,
    experience_years text,
    sources text,
    verticals text,
    solo_or_team text,
    educational text,
    top_offers text,
    connect_offers text,
    first_traffic text,
    first_payment text,
    froder text,
    feedback_push text,
    get_feedback text,
    stop_traffic_reason text,
    about_us text,
    google_sheets text)
    """)

    db.commit()
    db.close()

def add_new_table_2():
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(""" CREATE TABLE tg_hello_bot_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATE,
    chat_id integer not null, 
    username text not null,
    first_name text not null,
    last_name text not null
    )
    """)

    db.commit()
    db.close()



def copy_table():
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    db_res = cur.execute("""INSERT INTO novoreg_test SELECT * FROM novoreg2""")

    db.commit()
    db.close()


def add_column():
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    db_res = cur.execute("""ALTER TABLE novoreg ADD COLUMN google_sheets TEXT;""")

    db.commit()
    db.close()


"""" affise_get_new_partners.py """


def add_new_partner(partner):
    status = 'no_chat'  # good_chat, noob
    target = 'True'
    partner_id = int(partner['id'])
    created_at = partner['created_at']
    ref_id = ""
    email = str(partner['email'])
    telegram = ""
    experience = ""
    verticals = ""
    sources = ""
    about_us = ""
    phone = ""
    another_contacts = ""

    for key in partner:
        if key == 'ref_id':
            ref_id = int(partner['ref_id'])
        elif key == 'experience':
            experience = f"{partner['experience']})"
        elif key == 'verticals':
            verticals = f"{partner['verticals']}"
        elif key == 'sources':
            sources = f"{partner['sources']}"
        elif key == 'about_us':
            about_us = f"{partner['about_us']}"
        elif key == 'telegram':
            telegram = str(partner['telegram'])
        elif key == 'phone':
            phone = partner['phone']
        elif key == 'another_contacts':
            another_contacts = partner['another_contacts']

    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(f"""INSERT INTO novoreg_main (status, target, partner_id, created_at, ref_partner, email, phone, vk, telegram, experience,
                                        verticals, sources, about_us)
                                                  
                                        VALUES ('{status}', '{target}', '{partner_id}', '{created_at}',
                                                '{ref_id}', '{email}', '{phone}', '{another_contacts}', '{telegram}',
                                                '{experience}', '{verticals}', '{sources}', '{about_us}')""")
    db.commit()
    db.close()
    return True


def get_partners_id():
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    db_res = cur.execute("SELECT partner_id FROM novoreg_main").fetchall()
    res = tuple(i[0] for i in db_res)
    db.commit()
    db.close()

    return res

"""" hello.py """

def get_partners_for_hello():
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    db_res = cur.execute("SELECT partner_id, telegram, send_hello FROM novoreg_main WHERE send_hello is Null").fetchall()
    db.commit()
    db.close()
    partners_info_list = []

    for i in db_res:
        partner_info = {}
        partner_info['id'] = i[0]
        if 'https://t.me/' in i[1]:
            tg = str(i[1]).split('https://t.me/')
            partner_info['telegram'] = tg[1]
        else:
            partner_info['telegram'] = i[1]
        partner_info['send_hello'] = i[2]
        partners_info_list.append(partner_info)

    # for partner in partners_info_list:
    #     print(partner)
    return partners_info_list


def add_good_hello_status(partner_id):
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(f"UPDATE novoreg_main SET send_hello = 'True' WHERE partner_id = '{partner_id}'")

    db.commit()
    db.close()

    return True

def add_bad_hello_status(text_status, partner_id):
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(f"UPDATE novoreg_main SET tg_send_hello_error = '{text_status}', send_hello = 'False' WHERE partner_id = '{partner_id}'")

    db.commit()
    db.close()

    return True



"""" sheets_add_new_partners.py """
def get_partners_for_sheets():
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    db_res = cur.execute(
        f"SELECT status, partner_id, target, created_at, ref_partner, email, telegram, tg_send_hello_error, send_hello, experience, sources, verticals, about_us FROM novoreg_main WHERE google_sheets is Null").fetchall()

    # res = tuple(i[0] for i in db_res)
    partners_info_list = []
    for i in db_res:
        partner_info = {}
        partner_info['status'] = i[0]
        partner_info['id'] = i[1]
        partner_info['target'] = i[2]
        partner_info['created_at'] = i[3]
        partner_info['ref_partner'] = i[4]
        partner_info['email'] = i[5]
        partner_info['telegram'] = i[6]
        partner_info['tg_send_hello_error'] = i[7]
        partner_info['send_hello'] = i[8]
        partner_info['experience'] = i[9]
        partner_info['sources'] = i[10]
        partner_info['verticals'] = i[11]
        partner_info['about_us'] = i[12]
        partners_info_list.append(partner_info)

    db.commit()
    db.close()

    # for partner in partners_info_list:
    #     print(partner)
    return partners_info_list

def add_google_sheets_status(partner_id):
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    cur.execute(f"UPDATE novoreg_main SET google_sheets = 'True' WHERE partner_id = '{partner_id}'")
    db.commit()
    db.close()
    return True


def set_novoreg_status(partner_id: int, column: str, status: str):
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(f"UPDATE novoreg_main SET {column} = '{status}' WHERE partner_id = '{partner_id}'")

    db.commit()
    db.close()

    return True


def get_novoreg_status(partner_id: int, column: str):
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    res = cur.execute(f"SELECT {column} from novoreg_main WHERE partner_id = '{partner_id}'").fetchone()
    res = res[0]

    db.commit()
    db.close()

    return res

def get_all_partners():
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    db_res = cur.execute(f"SELECT * FROM novoreg").fetchall()
    # for partner in db_res:
    #     print(partner)

    partners_list = []
    partners_info_list = []

    for partner in db_res:
        partners_info = []
        for i in partner:
            if type(i) == str and len(i) == 0:
                i = None
            partners_info.append(i)
        partners_list.append(partners_info)
    for partner in partners_info_list:
        print(partner)

    for i in partners_list:
        partner_info = {}
        partner_info['status'] = i[1]
        partner_info['partner_id'] = i[2]
        partner_info['target'] = i[3]
        partner_info['created_at'] = i[4]
        partner_info['name'] = i[5]
        partner_info['ref_partner'] = i[6]
        partner_info['email'] = i[7]
        partner_info['phone'] = i[8]
        partner_info['vk'] = i[9]
        partner_info['skype'] = i[10]
        partner_info['telegram'] = i[11]
        partner_info['country'] = i[12]
        partner_info['alter_send_hello'] = i[13]
        partner_info['tg_send_hello_error'] = None
        partner_info['send_hello'] = i[14]
        partner_info['hello_answer'] = i[15]
        partner_info['second_hello'] = i[16]
        partner_info['third_hello'] = None
        partner_info['read_no_answer'] = i[17]
        partner_info['no_read'] = i[18]
        partner_info['second_hello_answer'] = None
        partner_info['segment'] = None
        partner_info['form'] = i[19]
        partner_info['answers'] = i[20]
        partner_info['experience'] = i[21]
        partner_info['experience_years'] = None
        partner_info['sources'] = i[22]
        partner_info['verticals'] = i[23]
        partner_info['solo_or_team'] = None
        partner_info['educational'] = i[24]
        partner_info['top_offers'] = i[25]
        partner_info['connect_offers'] = i[26]
        partner_info['first_traffic'] = i[27]
        partner_info['first_payment'] = None
        partner_info['froder'] = None
        partner_info['feedback_push'] = None
        partner_info['get_feedback'] = None
        partner_info['stop_traffic_reason'] = None
        partner_info['about_us'] = i[28]
        partner_info['google_sheet'] = i[29]

        partners_info_list.append(partner_info)

    db.commit()
    db.close()
    # for i in partners_info_list:
    #     print(i)
    return partners_info_list

def insert_partners_info(partner):
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    cur.execute(f"""INSERT INTO novoreg2 (status, partner_id, target, created_at, name, ref_partner, email, phone,
    vk, skype, telegram, country, alter_send_hello, tg_send_hello_error, send_hello, hello_answer, second_hello, third_hello,
    read_no_answer, no_read, second_hello_answer, segment, form, answers, experience, experience_years, sources, verticals,
    solo_or_team, educational, top_offers, connect_offers, first_traffic, first_payment, froder, feedback_push, get_feedback,
    stop_traffic_reason, about_us)        
                                          VALUES ('{partner['status']}', '{partner['partner_id']}', '{partner['target']}',
    '{partner['created_at']}', '{partner['name']}', '{partner['ref_partner']}', '{partner['email']}', '{partner['phone']}', 
    '{partner['vk']}', '{partner['skype']}', '{partner['telegram']}', '{partner['country']}', '{partner['alter_send_hello']}',
    '{partner['tg_send_hello_error']}', '{partner['send_hello']}', '{partner['hello_answer']}', '{partner['second_hello']}',
    '{partner['third_hello']}', '{partner['read_no_answer']}', '{partner['no_read']}', '{partner['second_hello_answer']}',
    '{partner['segment']}', '{partner['form']}', '{partner['answers']}', '{partner['experience']}', '{partner['experience_years']}',
    '{partner['sources']}', '{partner['verticals']}', '{partner['solo_or_team']}', '{partner['educational']}',
    '{partner['top_offers']}', '{partner['connect_offers']}', '{partner['first_traffic']}', '{partner['first_payment']}',
    '{partner['froder']}', '{partner['feedback_push']}', '{partner['get_feedback']}', '{partner['stop_traffic_reason']}',
    '{partner['about_us']}')""")

    db.commit()
    db.close()



def get_update_partner_for_sheets(partner_id):
    db = sqlite3.connect('novoreg.db')
    cur = db.cursor()
    db_res = cur.execute(
        f"""SELECT status, partner_id, target, created_at, name, ref_partner, email, telegram, send_hello, hello_answer, segment, 
        form, experience, experience_years, sources, verticals, solo_or_team, connect_offers, about_us FROM novoreg_main WHERE partner_id = {partner_id}""").fetchone()
    # res = tuple(i[0] for i in db_res)
    db.commit()
    db.close()
    if db_res is not None:
        partner_info = {'status': db_res[0], 'partner_id': db_res[1], 'target': db_res[2], 'created_at': db_res[3], 'name':db_res[4], 'ref_partner': db_res[5],
                            'email': db_res[6], 'telegram': db_res[7], 'send_hello': db_res[8], 'hello_answer': db_res[9], 'segment': db_res[10],
                            'form': db_res[11], 'experience': db_res[12], 'experience_years': db_res[13], 'sources': db_res[14], 'verticals': db_res[15],
                            'solo_or_team': db_res[16], 'connect_offers': db_res[17], 'about_us': db_res[18]}
        return partner_info
    else:
        return None

def update_partner_status(partner: dict):
    status = 'good_chat'
    name = partner['name']
    experience = partner['experience']
    verticals = partner['verticals']
    sources = partner['sources']
    experience_years = partner['experience_years']
    segment = partner['segment']
    if 'solo_or_team' in partner:
        solo_or_team = partner['solo_or_team']
    else:
        solo_or_team = None
    if 'about_us' in partner:
        about_us = partner['about_us']
    else:
        about_us = None
    form = 'True'
    hello_answer = 'True'
    db = sqlite3.connect('../database/novoreg.db')
    cur = db.cursor()
    cur.execute(f"""UPDATE novoreg_main  SET status = '{status}', name = '{name}', experience = '{experience}', 
                                               verticals = '{verticals}', sources = '{sources}', 
                                               experience_years = '{experience_years}', segment = '{segment}',
                                               solo_or_team = '{solo_or_team}', about_us = '{about_us}',
                                               form = '{form}', hello_answer = '{hello_answer}' WHERE partner_id = '{partner['partner_id']}'""")
    db.commit()
    db.close()

####################################################################

def get_old_status(partner_id): # тест
    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    db_res = cur.execute(
        f"SELECT status, partner_id, target, created_at, ref_partner, email, telegram, send_hello, experience, sources, verticals, connect_offers, about_us FROM novoreg_test WHERE partner_id = {partner_id}").fetchall()

    # res = tuple(i[0] for i in db_res)
    partners_info_list = []
    partner_info = {}
    for i in db_res:
        partner_info['status'] = i[0]
        partner_info['id'] = i[1]
        partner_info['target'] = i[2]
        partner_info['created_at'] = i[3]
        partner_info['ref_partner'] = i[4]
        partner_info['email'] = i[5]
        partner_info['telegram'] = i[6]
        partner_info['send_hello'] = i[7]
        partner_info['experience'] = i[8]
        partner_info['sources'] = i[9]
        partner_info['verticals'] = i[10]
        partner_info['connect_offers'] = i[11]
        partner_info['about_us'] = i[12]
        # partners_info_list.append(partner_info)

    db.commit()
    db.close()
    return partner_info

def get_partner_id():


    db = sqlite3.connect('../database/novoreg.db')

    cur = db.cursor()

    no_sheets_list = (33090, 33091, 33092, 33093,
33089,
33088,
33087,
33086,
33085,
33084,
33083,
33082,
33081,
33080,
33079,
33078,
33077,
33076,
33075,
33074,
33073,
33072)


    db_res = cur.execute(f"SELECT partner_id FROM novoreg_main").fetchall()
    res = tuple(i[0] for i in db_res)

    for i in res:
        if i in no_sheets_list:
            continue
        else:
            cur.execute(f"UPDATE novoreg_main SET send_hello = 'True' WHERE partner_id = {i}")
    db.commit()
    db.close()
    return res

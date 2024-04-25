from affise_get_new_partners import affise_get_new_partners
from hello import hello_sendler
import time

from novoreg_table.logs import logger as log

from sheets_add_new_partners import sheets_add_new_partners

if __name__ == "__main__":
    while True:
        affise_get_new_partners()
        hello_sendler()
        sheets_add_new_partners()
        log.msg.info('Спим 5  минут  и повторяем попытку')
        # print('Спим 5  минут  и повторяем попытку')
        time.sleep(300)



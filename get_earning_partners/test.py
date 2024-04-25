



date_list = [{'date': '2023-10-29 00:21:09', 'partner': 31914, 'ref_partner': 27279},
             {'date': '2023-10-30 19:09:46', 'partner': 31938, 'ref_partner': 6713},
             {'date': '2023-11-06 21:26:28', 'partner': 32027, 'ref_partner': 25461},
             {'date': '2023-12-01 10:34:51', 'partner': 32233, 'ref_partner': 29772},
             {'date': '2023-12-08 15:50:30', 'partner': 32298, 'ref_partner': 24033},
             {'date': '2023-12-11 18:18:16', 'partner': 32321, 'ref_partner': 24033},
             {'date': '2023-12-11 19:59:09', 'partner': 32324, 'ref_partner': 24033},
             {'date': '2023-12-12 10:21:10', 'partner': 32326, 'ref_partner': 24033},
             {'date': '2022-12-12 11:39:18', 'partner': 32328, 'ref_partner': 24033},
             {'date': '2023-12-12 15:20:04', 'partner': 32332, 'ref_partner': 24033},
             {'date': '2023-12-20 14:54:15', 'partner': 32405, 'ref_partner': 7410},
             {'date': '2021-12-24 18:06:01', 'partner': 32443, 'ref_partner': 32427}]

for i in date_list:
    if '2022' in i['date'] or '2021' in i['date']:
        print(i)
    # elif  in i['date']:
    #     print(i)
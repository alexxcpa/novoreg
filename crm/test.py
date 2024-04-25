import requests


url1 = f'https://lead-magnet.bitrix24.ru/rest/456/ks0qtwhiibznzc85/crm.lead.fields.json' # какие поля вовзращает лид

url2 = ""


# headers = {'API-Key': AFFISE_API_KEY}
print(f"Запрос в аффайз за период ")
r = requests.get(url)
res = r.json()

print(res)
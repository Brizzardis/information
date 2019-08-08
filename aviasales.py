from pprint import pprint
import requests
import json

from_city = input('Город отправления: ')
to_city = input('Город прибытия: ')

iata_link = f'https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{from_city}%20в%20{to_city}'
iata_req = requests.get(iata_link)
iata_data = json.loads(iata_req.text)
from_city = iata_data['origin']['iata']
to_city = iata_data['destination']['iata']

service = 'http://min-prices.aviasales.ru/calendar_preload?'
way = input('Обратный билет(да\нет): ')

if way == 'да':
    price_link = f'{service}origin={from_city}&destination={to_city}'
if way == 'нет':
    price_link = f'{service}origin={from_city}&destination={to_city}&one_way=true'

price_req = requests.get(price_link)
price_data = json.loads(price_req.text)
result = []
for i in price_data['best_prices']:
    result.append([i['origin'], i['destination'], i['value'], i['depart_date'], i['return_date'], i['gate']])
result.sort()
pprint(result)

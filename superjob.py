from bs4 import BeautifulSoup as bs
import requests


html = requests.get('https://www.superjob.ru/vakansii/programmist.html').text

parsed_html = bs(html,'html.parser')

data_list = parsed_html.findAll("div", {"class": "_3zucV _2GPIV i6-sc _3VcZr"})

list_job = []

for i in data_list:
    name = i.find('div', {'class': '_3mfro'}).text
    salary = i.find('span', {'class': 'f-test-text-company-item-salary'}).text
    link = i.find('a', {'class': 'icMQ_'})
    link = 'https://www.superjob.ru' + link['href']

    list_job.append(name + ' ' + salary + ' ' + link)

for i in list_job:
    print(i)

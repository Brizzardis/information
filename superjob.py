from bs4 import BeautifulSoup as bs
import requests


vacancy = input('Введите язык программирования для поиска вакансий: ')

def get_vacancy(page):
    if vacancy:
        link = f'https://www.superjob.ru/vakansii/programmist-{vacancy}.html?geo%5Bc%5D%5B0%5D=1&page={page}'
    else:
        link = f'https://www.superjob.ru/vakansii/programmist.html?geo%5Bc%5D%5B0%5D=1&page={page}'
    html = requests.get(link).text
    return html


for i in range(1, 6):
    parsed_html = bs(get_vacancy(i), 'html.parser')

    data_list = parsed_html.findAll("div", {"class": "_3zucV _2GPIV i6-sc _3VcZr"})

    list_job = []

    for i in data_list:
        name = i.find('div', {'class': '_3mfro'}).text
        salary = i.find('span', {'class': 'f-test-text-company-item-salary'}).text
        link = i.find('a', {'class': 'icMQ_'})
        link = 'https://www.superjob.ru' + link['href']
        print(name + ". " + salary + " " + link + '\n')

from bs4 import BeautifulSoup as bs
import requests
#import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pymongo import MongoClient

vacancy = input('Введите язык программирования для поиска вакансий (для показа всех вакансий "программист" - enter): ')

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['vacancy']
vacancy_db = db.vacancy

def new_vacancy(title, salary_min, salary_max, link):
    vacancy_db.insert_one({
        'title': title,
        'salary_min': salary_min,
        'salary_max': salary_max,
        'link': link
    })
    if salary_min == 'По договорённости' or salary_min == 'з/п не указана' or salary_min == salary_max:
        print(f'Добавлена новая вакансия: {title}, {salary_min}, {link}')
    else:
        print(f'Добавлена новая вакансия: {title}, {salary_min}-{salary_max}, {link}')


def get_currency(salary):
    currency = re.search('(EUR|USD|руб|₽)', salary)
    if currency == None:
        return 'з/п не указана'
    elif currency.group(1) == 'EUR':
        return 73
    elif currency.group(1) == 'USD':
        return 66
    elif currency.group(1) == 'руб':
        return 1
    elif currency.group(1) == '₽':
        return 1


# Сбор данных с hh
# Ошибка максимального количества подключений через get-запрос, поэтому селениум

def wait(method, name):
    waiting = WebDriverWait(driver, 20).until(EC.presence_of_element_located((method, name)))


driver = webdriver.Chrome()
html = driver.get(
    f'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_field=name&text=программист{vacancy}&area=113&from=cluster_area&showClusters=true')
assert 'hh.ru' in driver.title

for i in range(1, 6):
    wait(By.CLASS_NAME, 'vacancy-serp-item')
    # time.sleep(1)
    vacancies_list = driver.find_elements_by_class_name('vacancy-serp-item')
    vacancy_dict_list = {}
    for i in vacancies_list:
        # time.sleep(1)
        title = i.find_element_by_class_name('bloko-link').text
        link = i.find_element_by_class_name('bloko-link')
        link = link.get_attribute('href')

        salary = i.find_element_by_class_name('vacancy-serp-item__sidebar').text

        if get_currency(salary) == 'з/п не указана':
            salary_min = get_currency(salary)
            salary_max = get_currency(salary)
        else:
            salary_min = re.search('([0-9]{1,3})\s([0-9]{3})', salary)
            salary_min = int(salary_min.group(1) + salary_min.group(2)) * get_currency(salary)
            salary_max = re.search('[0-9]{1,3}\s[0-9]{3}-([0-9]{1,3})\s([0-9]{3})', salary)
            if salary_max != None:
                salary_max = int(salary_max.group(1) + salary_max.group(2)) * get_currency(salary)
            else:
                salary_max = salary_min

        new_vacancy(title, salary_min, salary_max, link)

    driver.delete_all_cookies()

    wait(By.CLASS_NAME, 'HH-Pager-Controls-Next')
    button = driver.find_element_by_class_name('HH-Pager-Controls-Next')
    button.send_keys(Keys.RETURN)

driver.quit()


# сбор данных с superjob


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

    for i in data_list:
        title = i.find('div', {'class': '_3mfro'}).text
        salary = i.find('span', {'class': 'f-test-text-company-item-salary'}).text
        if salary == 'По договорённости':
            salary_min = 'По договорённости'
            salary_max = 'По договорённости'
        else:
            salary_min = re.search('([0-9]{1,3})\s([0-9]{3})', salary)
            salary_max = re.search('([0-9]{1,3})\s([0-9]{3})\s₽$', salary)
            if salary_min != salary_max:
                salary_min = int(salary_min.group(1) + salary_min.group(2)) * get_currency(salary)
                salary_max = int(salary_max.group(1) + salary_max.group(2)) * get_currency(salary)
            else:
                salary_min = int(salary_min.group(1) + salary_min.group(2)) * get_currency(salary)
                salary_max = salary_min
        link = i.find('a', {'class': 'icMQ_'})
        link = 'https://www.superjob.ru' + link['href']

        new_vacancy(title, salary_min, salary_max, link)

def filter_salary():
    filter = int(input("Введите минимальную зарплату для отображения: "))
    for i in vacancy_db.find({"salary_min": {"$ne": "з/п не указана"}} and {"salary_min": {"$ne": "По договорённости"}} and {"salary_min": {"$gte": filter}}):
        print(i)

filter_salary()

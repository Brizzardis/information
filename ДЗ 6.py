from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time


def wait(method, name):
    waiting = WebDriverWait(driver, 20).until(EC.presence_of_element_located((method, name)))


def get_email(message):
    wait(By.CLASS_NAME, 'mail-Message-Sender-Email')
    data = driver.find_element_by_class_name('mail-Message-Sender-Email').text
    return data


def get_date(message):
    wait(By.CLASS_NAME, 'ns-view-message-head-date')
    data = driver.find_element_by_class_name('ns-view-message-head-date').text
    return data


def get_theme(message):
    wait(By.CLASS_NAME, 'mail-Message-Toolbar-Subject')
    data = driver.find_element_by_class_name('mail-Message-Toolbar-Subject').text
    return data


def get_text(message):
    wait(By.TAG_NAME, 'p')
    text_list = driver.find_elements_by_tag_name('p')
    data = ''
    for i in text_list:
        data = data + '\n' + i.text
    return data


def write(message):
    email = get_email(message)
    date = get_date(message)
    theme = get_theme(message)
    text = get_text(message)

    messages_db.insert_one({
        'email': email,
        'date': date,
        'theme': theme,
        'text': text
    })
    print('Запись успешно создана!')


driver = webdriver.Chrome()
driver.get(
    'https://passport.yandex.ru/auth?from=mail&origin=hostroot_homer_auth_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fmail.yandex.ru%3Fnoretpath%3D1')
assert 'Авторизация' in driver.title
elem = driver.find_element_by_id('passp-field-login')
elem.send_keys('ilyabrilenkov2013@yandex.ru')
elem.send_keys(Keys.RETURN)

wait(By.ID, 'passp-field-passwd')

elem = driver.find_element_by_id("passp-field-passwd")
elem.send_keys('789123789123')
elem.send_keys(Keys.RETURN)

wait(By.CLASS_NAME, 'ns-view-right-box')

message = driver.find_element_by_class_name('ns-view-messages-item-wrap')
message.click()

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['messages']
messages_db = db.messages

for i in range(11):
    write(message)
    wait(By.CLASS_NAME, 'mail-Message-PrevNext_next')
    button = driver.find_element_by_class_name('mail-Message-PrevNext_next')
    button.click()
    if button.click():
        True
    else:
        time.sleep(1)
    # сделал через sleep, потому что функция write работала быстрее кнопки и отрабатывала два раза на каждом письме,
    # а затем на 3-4 вылетало с ошибкой. Не смог понять из-за чего так и сделал 1 секунду сон.
    # Теоретически и кнопка и текст на одной странице, но или кнопка дольше грузится, или я что-то упустил

objects = messages_db.find()
for i in objects:
    print(i)

driver.quit()

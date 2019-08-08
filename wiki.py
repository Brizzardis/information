from pprint import pprint
import requests
import re

def get_link(topic):
    link='https://ru.wikipedia.org/wiki/'+topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html = requests.get(link).text
    return html


def get_topic_text(topic):
    words = re.findall("[а-яА-Яё]{3,}", topic)
    return words


def get_common_words(topic):
    words_list = get_topic_text(topic)
    rate = {}
    for word in words_list:
        if word in rate:
            rate[word] += 1
        else:
            rate[word] = 1
    rate_list = list(rate.items())
    rate_list.sort(key=lambda x: -x[1])
    return rate_list

dict1 = get_topic_page('Дерево')

link = re.findall('<li><a rel="nofollow" class="external text" '
 'href=".+"', dict1)

num = 1
for i in link:
    req_link = re.findall('http.+\\b', i)
    html = requests.get(req_link[0]).text
    result = get_common_words(html)
    print(result)
    with open(f'file_{num}.txt', 'w') as file:
        file.write('\n'.join('%s %s' % x for x in result))
    num += 1

print(f'Количество ссылок = {num - 1}')








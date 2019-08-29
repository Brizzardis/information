import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('opendata.csv', encoding='windows-1251')

data_type = input('Введите тип данных: ')
date_from = input('Введите начальную дату через пробел:(год-месяц-число) ')
date_to = input('Введите конечную дату через пробел:(год-месяц-число) ')
region = input('Введите регион: ')

data = data.loc[data['name'] == data_type].loc[data['date'] >= date_from].loc[data['date'] <= date_to].loc[data['region'] == region]
print(data)

plt.plot(data['date'], data['value'])
plt.show()

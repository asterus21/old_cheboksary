import time
import requests
import urllib.request
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup

start = time.time()

def get_photo():

	pictures, names = [], []
	#check range from 0 up to 225000 but not all values at once
	for i in range(10001, 20001):

		page = requests.get(f'https://foto.cheb.ru/foto/{i}.htm')
		soup = BeautifulSoup(page.text, 'lxml')
		content = soup.prettify()

		if 'Историческое' in content:

			photos_names = soup.find_all('h1')
			for name in photos_names:
				if name != 'Ошибка: фотография не найдена' or name != 'Ошибка: страница не найдена' or name != '':
					names.append(name.text)
				else:
					continue

			photos = soup.select('.i-img')
			for photo in photos:
				pictures.append(photo['src'])

	url = ['https://foto.cheb.ru' + picture for picture in pictures]
	dict_ = dict(zip(names,url))

	for url_ in url:
		urllib.request.urlretrieve(url_, url_.split("-")[-1])

	df = pd.DataFrame.from_dict(dict_, orient = 'index', columns = ['Link'])
	df.to_excel('index.xlsx')

	#you can't name a file in Windows 10 using quotes or slashes!

	print(len(url))
	print(dict_)

get_photo()

print("--- %s seconds ---" % (time.time() - start))

#TODO: Создать CSV-файл или Excel-файл с индексом для удобства редактирования скаченных файлов
#TODO: Скачать фото в созданную заранее папку, назвать фото по ключу из словаря dict_ (см. библиотеку os)

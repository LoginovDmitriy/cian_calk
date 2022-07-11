# получить id объявлений
# пройтись циклом по ссылкам и забрать:
	# -адрес
	# -площадь
	# -тип квартиры
	# -цену
	# -этаж/этажность
#записываем эти данные в словарь

# собираем ссулку на рассчет цены в циане
# пробегаем циклом дописываем в словарь оценочную стоимость


import requests
from bs4 import BeautifulSoup
import io

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class Bot:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument("user-data-dir=C:\\Users\\Дмитрий\\AppData\\Local\\Google\\Chrome\\User Data")
		self.driver = webdriver.Chrome(chrome_options=options) 


		# options = webdriver.ChromeOptions()
		# chrome_options = Options()
		# options.add_argument("user-data-dir=C:\\hrome\\Default") #Path to your chrome profile
		#                                   # C:\\Users\\про\\AppData\\Local\\Google\\Chrome\\User Data\\Default
		# # self.driver = webdriver.Chrome(executable_path="C:\\Files\\chromedriver.exe", chrome_options=options)		
		# self.driver = webdriver.Chrome(executable_path=r'C:\\Files\\chromedriver.exe', chrome_options=options)
		self.navigate()
	
	def navigate(self):
		f = open('url.txt')
		for url in f.readlines():
		# url = 'https://www.domofond.ru/3-komnatnaya-kvartira-na-prodazhu-sankt_peterburg-3847827434'
		# self.driver.get('https://www.domofond.ru/')
			try:
				a = get_page_data(get_html(url.strip()), url.strip())
				self.driver.get(a[-1])
				# sleep(2000)
				source_data = self.driver.page_source
				soup = BeautifulSoup(source_data, 'lxml')
				cian_price = soup.find('div', class_='ddf61b4218--item--68Z1X').find('span', class_='ddf61b4218--color_black_100--A_xYw ddf61b4218--lineHeight_28px--3QLml ddf61b4218--fontWeight_bold--t3Ars ddf61b4218--fontSize_22px--3UVPd ddf61b4218--display_block--1eYsq ddf61b4218--text--2_SER').text
				cian_price.replace(' ', '')
				cian_price = cian_price[:-1]
				new_price = int(cian_price.replace(' ',''))*a[2]
				profit = int(new_price) - int(a[1])
				if profit>0:
					print(url)
					print('Старая цена - ',  a[1])
					print('Оценочная стоимость - ', new_price)
					print('Прибыль - ', profit)
				sleep(2)
				cian_price=0
			except:
				pass



def get_html(url):
	r = requests.get(url)
	return r.text

def get_page_data(html, url): #собирает данные квартиры из объявления
	soup = BeautifulSoup(html, 'lxml')
	# print(soup)
	flat_data = soup.find('h5', class_='description__title___2N9Wk').text
	flat_data = flat_data.split(',')
	f_type = flat_data[0].strip()[0]
	if f_type == 'К':
		f_type='1'
	area = flat_data[1].strip().replace(' м²', '')
	floor = flat_data[2].strip().replace(' эт.', '')
	price = soup.find('div', class_='information__price___2Lpc0').text
	price = price.replace(' ', '')[:-1]
	adress = soup.find('p', class_='location__text___bhjoZ').text
	str_data = url +'\n' + f_type +'\n'+ area +'\n' + floor +'\n' + price +'\n'+ adress +'\n'
	# print(str_data)
	adress = adress.replace(' ', '%20')
	data = []
	# get_cian_price(adress, area, f_type)
	url_cian = 'https://spb.cian.ru/kalkulator-nedvizhimosti/?address='+adress+'&totalArea='+area+'&roomsCount='+f_type
	data.append(url)
	data.append(int(price))
	data.append(int(area))
	data.append(adress)
	data.append(floor)
	data.append(url_cian)
	return data

# def get_cian_price(adress, area, f_type): #get cian price
# 	url_cian = 'https://spb.cian.ru/kalkulator-nedvizhimosti/?address='+adress+'&totalArea='+area+'&roomsCount='+f_type
# 	# print(url_cian)
# 	soup = BeautifulSoup(get_html(url_cian), 'lxml')
# 	print(soup)
# 	cian_price = soup.find('div', class_='ddf61b4218--item--68Z1X').find('span').text
# 	print('Цена по данным ЦИАН - '+cian_price)
def main():
	url = 'https://www.domofond.ru/3-komnatnaya-kvartira-na-prodazhu-sankt_peterburg-3847827434'
	# print(get_page_data(get_html(url), url))
	b = Bot()
	# get_cian_price()
	# f = open('url.txt')
	# for line in f.readlines():
	# 	try:
	# 		get_page_data(get_html(line.strip()), line.strip())
	# 	except:
	# 		print('Не загружено', line)

if __name__ == '__main__':
	main()
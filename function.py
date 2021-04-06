import datetime
import math
import time
from selenium  import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os

import db

# -- open browser
options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized")  
driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com/")

# --------1 Diaonline
def scrape_categ_dia(url):
	data = []
	driver.get(url)
	for x in range(1, 11):
		categ_main_name = driver.find_element_by_xpath('//*[@id="appVue"]/header/div[3]/div/nav[1]/ul/li[1]/div/ul/li[' + str(x) + ']/a/span').get_attribute('textContent').strip()
		categ_main_url = driver.find_element_by_xpath('//*[@id="appVue"]/header/div[3]/div/nav[1]/ul/li[1]/div/ul/li[' + str(x) + ']/a').get_attribute('href')
		print('-----' + categ_main_name)
		try:
			categ_branch_content = driver.find_element_by_xpath('//*[@id="appVue"]/header/div[3]/div/nav[1]/ul/li[1]/div/ul/li[' + str(x) + ']/div/div[2]/div[1]').find_elements_by_class_name('bloque__col')
			for categ_branch in categ_branch_content:
				try:
					categ_branch_name = categ_branch.find_element_by_tag_name('h6').find_element_by_tag_name('a').get_attribute('textContent').strip()
					print(categ_branch_name)
					branch_url = categ_branch.find_element_by_tag_name('h6').find_element_by_tag_name('a').get_attribute('href')
					data.append((1,categ_main_name, categ_branch_name, branch_url))
				except:
					print("except!")
		except:
			print('except! 5')
			data.append((1,categ_main_name, '', categ_main_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket, categ_main, categ_branch, url","%s,%s,%s,%s",data)

# --------2 Walmart
def scrape_categ_walmart(url):
	data = []
	driver.get(url)
	action = ActionChains(driver)
	parent_level_menu = driver.find_element_by_xpath('//*[@id="header-root"]/div/div/div[1]/div/div/nav/button')
	action.move_to_element(parent_level_menu).perform()
	for x in range(3, 10):
		categ_main_name = driver.find_element_by_xpath('//*[@id="header-root"]/div/div/div[1]/div/div/nav/div/div/div/div[1]/ul/li[' + str(x) + ']/span').get_attribute('textContent').strip()
		categ_main_content = driver.find_element_by_xpath('//*[@id="header-root"]/div/div/div[1]/div/div/nav/div/div/div/div[' + str(x - 1) + ']').find_elements_by_tag_name('ul')
		print(categ_main_name)
		print(len(categ_main_content))
		for i in range(1, len(categ_main_content)):
			categ_branch_name = categ_main_content[i].find_element_by_class_name('header-categories-nav__categorie-parent').find_element_by_tag_name('a').get_attribute('textContent').strip()
			branch_url = categ_main_content[i].find_element_by_class_name('header-categories-nav__categorie-parent').find_element_by_tag_name('a').get_attribute('href')
			data.append((2,categ_main_name, categ_branch_name, branch_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket, categ_main, categ_branch, url","%s,%s,%s,%s", data)

# --------3 Jumbo
def scrape_categ_jumbo(url):
	data = []
	driver.get(url)
	sleep(5)
	for x in range(13):	
		categ_main_name = driver.find_elements_by_xpath('//*[@id="department-wrapper"]/child::div[@class="item food"]')[x].find_element_by_tag_name('a').get_attribute('textContent').strip()
		categ_branch_content = driver.find_elements_by_xpath('//*[@id="category-wrapper"]/div[' + str(x + 2) + ']/div[@class="categories"]/div[@class="item-wrapper"]/child::div')
		print('---------' + categ_main_name)
		for i in range(0, len(categ_branch_content)):
			categ_branch_name = categ_branch_content[i].find_element_by_tag_name('a').get_attribute('textContent').strip()
			branch_url = categ_branch_content[i].find_element_by_tag_name('a').get_attribute('href')
			data.append((3, categ_main_name, categ_branch_name, branch_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket,categ_main,categ_branch,url","%s,%s,%s,%s",data)

# --------4 Disco
def scrape_categ_disco(url):
	data = []
	driver.get(url)
	sleep(5)
	for x in range(2, 13):	
		categ_main_name = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/p').get_attribute('textContent').strip()
		categ_branch_content = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/div/ul').find_elements_by_tag_name('li')
		categ_child_content = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/div/div').find_elements_by_class_name('sub-categorias-contenido-container')
		print('---------'+categ_main_name)
		for i in range(1, len(categ_branch_content)):
			categ_branch_name = categ_branch_content[i].find_element_by_tag_name('p').get_attribute('textContent').strip()
			print('!'+categ_branch_name)
			child_length = len(categ_child_content[i - 1].find_elements_by_tag_name('li'))
			child_url = ''
			if child_length == 0:
				child_id = categ_branch_content[i].get_attribute('data-id')
				child_url = '//li[@data-id="'+ child_id +'"]'
				data.append((4,categ_main_name, categ_branch_name, child_url))
			else:
				for categ_child in categ_child_content[i - 1].find_elements_by_tag_name('li'):
					child_id = categ_child.get_attribute('data-second-level-id')
					child_url = '//p[@data-idmenu="'+ child_id +'"]'
					data.append((4,categ_main_name, categ_branch_name, child_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket,categ_main,categ_branch,url","%s,%s,%s,%s",data)

# --------5 Coto
def scrape_categ_coto(url):
	data = []
	driver.get(url)
	sleep(5)
	for x in range(1, 6):	
		categ_main_name = driver.find_elements_by_xpath('//*[@id="atg_store_catNav"]/child::li')[x].find_element_by_tag_name('a').get_attribute('textContent').strip()
		categ_branch_content = driver.find_element_by_xpath('//*[@id="atg_store_catNav"]/child::li['+ str(x + 1) +']/div').find_elements_by_class_name('g1')
		print('---------' + categ_main_name)
		print(len(categ_branch_content))
		for i in range(0, len(categ_branch_content)):
			categ_branch_name = categ_branch_content[i].find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute('textContent').strip().split('(+)')[0]
			print(categ_branch_name)
			branch_url = categ_branch_content[i].find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute('href')
			print(branch_url)
			data.append((5, categ_main_name, categ_branch_name, branch_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket,categ_main,categ_branch,url","%s,%s,%s,%s",data)

# --------6 Carrefour
def scrape_categ_carrefour(url):
	data = []
	driver.get(url)
	sleep(5)
	for x in range(6, 20):	
		categ_main_content = driver.find_element_by_xpath('//*[@id="nav"]/ol/child::li[' + str(x) + ']/h2/a')
		categ_main_name = categ_main_content.get_attribute('textContent').strip().split(categ_main_content.find_element_by_tag_name('i').get_attribute('textContent').strip())[0]
		categ_branch_content = driver.find_elements_by_xpath('//*[@id="nav"]/ol/child::li[' + str(x) + ']/div[@class="ul-wrapper"]/ul/child::li')
		for i in range(2, len(categ_branch_content) - 1):
			categ_branch_name = categ_branch_content[i].find_element_by_tag_name('a').get_attribute('textContent').strip()
			branch_url = categ_branch_content[i].find_element_by_tag_name('a').get_attribute('href')
			data.append((6, categ_main_name, categ_branch_name, branch_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket,categ_main,categ_branch,url","%s,%s,%s,%s",data)

# --------7 Vea
def scrape_categ_vea(url):
	data = []
	driver.get(url)
	sleep(5)
	for x in range(2, 13):	
		categ_main_name = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/p').get_attribute('textContent').strip()
		categ_branch_content = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/div/ul').find_elements_by_tag_name('li')
		categ_child_content = driver.find_element_by_xpath('//*[@id="main_menu_categorias_list"]/li[' + str(x) + ']/div/div/div').find_elements_by_class_name('sub-categorias-contenido-container')
		print('---------'+categ_main_name)
		for i in range(1, len(categ_branch_content)):
			categ_branch_name = categ_branch_content[i].find_element_by_tag_name('p').get_attribute('textContent').strip()
			print('!'+categ_branch_name)
			child_length = len(categ_child_content[i - 1].find_elements_by_tag_name('li'))
			child_url = ''
			if child_length == 0:
				child_id = categ_branch_content[i].get_attribute('data-id')
				child_url = '//li[@data-id="'+ child_id +'"]'
				data.append((7,categ_main_name, categ_branch_name, child_url))
			else:
				for categ_child in categ_child_content[i - 1].find_elements_by_tag_name('li'):
					child_id = categ_child.get_attribute('data-second-level-id')
					child_url = '//p[@data-idmenu="'+ child_id +'"]'
					data.append((7,categ_main_name, categ_branch_name, child_url))
	else:
		print("---End!")
	db.insert_data("tbl_category", "supermarket,categ_main,categ_branch,url","%s,%s,%s,%s",data)

# --------1 Dia Product Scrape
product = []
def scrape_product_dia_inner(categ_id):
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(2)
		new_height = driver.execute_script('return document.body.scrollHeight')
		if new_height == last_height:
			try:
				driver.find_element_by_class_name('cargarMas').click()
				sleep(2)
			except:
				break
		last_height = new_height
	product_content = driver.find_elements_by_xpath('//*[@id="appVue"]/div[2]/section/div/div/div/div/div/div[2]/div[2]/child::div')
	for group in product_content:
		rows = group.find_elements_by_tag_name('ul')
		for row in rows:
			row = row.find_elements_by_tag_name('li')
			for item in row:
				try:
					image = item.find_element_by_class_name('product__image').find_element_by_tag_name('img').get_attribute('src')
					name = item.find_element_by_class_name('product__head').find_element_by_tag_name('h4').text.strip()
					price = item.find_element_by_class_name('product__price').find_element_by_tag_name('h3').find_element_by_tag_name('p').text.strip()
					discount = ''
					try:
						discount = item.find_element_by_class_name('product__price').find_element_by_tag_name('h3').find_element_by_tag_name('strong').text.strip()
					except:
						discount = ''
					product.append((image, name, price, discount, categ_id))
				except:
					continue

def scrape_product_dia():
	categories = db.get_category('1')
	for category in categories:
		url = category[1]
		driver.get(url)
		id = category[0]
		scrape_product_dia_inner(id)
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]

# --------2 Walmart Product Scrape
def scrape_product_walmart_inner(index, categ_id):
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(3)
		new_height = driver.execute_script('return document.body.scrollHeight')
		if new_height == last_height:
			break
		last_height = new_height
	product_content = driver.find_elements_by_xpath('//div[@class="search-result"]/div/div[2]/div[1]/div/ul/child::li')
	for item in product_content:
		try:
			image = item.find_element_by_class_name('prateleira__image-link').find_element_by_tag_name('img').get_attribute('src')
			price = ''
			price = item.find_element_by_class_name('prateleira__content').find_elements_by_tag_name('a')[0].find_element_by_class_name('prateleira__best-price').get_attribute('textContent').strip()
			name = item.find_element_by_class_name('prateleira__content').find_elements_by_tag_name('a')[1].get_attribute('textContent').strip()
			discount = ''
			try:
				discount = item.find_element_by_class_name('prateleira__content').find_element_by_tag_name('a').find_element_by_class_name('prateleira__discount').get_attribute('textContent').strip()
			except:
				discount = ''
			product.append((image, name, price, discount, categ_id))
		except:
			continue
	pagination = driver.find_elements_by_xpath('//div[@class="search-result"]/div/div[3]/div[2]/ul/child::li')
	for page in pagination:
		try:
			item_txt = page.get_attribute('textContent').strip()
			if item_txt == str(index + 1):
				driver.execute_script("arguments[0].click();", page)
				sleep(5)
				print('success')
				index += 1
				scrape_product_walmart_inner(index, categ_id)
		except:
			print('no text!')

def scrape_product_walmart():
	categories = db.get_category('2')
	for category in categories:
		driver.get(category[1])
		categ_id = category[0]
		print(categ_id)
		scrape_product_walmart_inner(1, categ_id)
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]

# --------3 Jumbo Product Scrape
def scrape_product_jumbo_inner(categ_id):
	product = []
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(5)
		new_height = driver.execute_script('return document.body.scrollHeight')
		if new_height == last_height:
			break
		last_height = new_height
	product_content = driver.find_elements_by_xpath('//div[@class="main"]/div[2]/div[2]/div/ul/child::li')
	print(len(product_content))
	for i in range(0, len(product_content), 2):
		image = product_content[i].find_element_by_class_name('product-item__image-link').find_element_by_tag_name('img').get_attribute('src')
		price = ''
		try:
			price = product_content[i].find_element_by_class_name('product-prices__value').get_attribute('textContent').strip()
		except:
			print('except -> price')
		name = product_content[i].find_element_by_class_name('product-item__name').find_element_by_tag_name('a').get_attribute('textContent').strip()
		discount = ''
		try:
			discount = driver.find_element_by_xpath('//div[@class="main"]/div[2]/div[2]/div/ul/child::li['+ str(i+1) +']/div[1]/div[3]/div[starts-with(@class,"flag flag-mktc type-square")]').get_attribute('textContent').strip()
		except:
			discount = ''
		product.append((image, name, price, discount, categ_id))
	else:
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		product.clear()

def scrape_product_jumbo():
	categories = db.get_category('3')
	for category in categories:
		driver.get(category[1])
		sleep(5)
		categ_id = category[0]
		scrape_product_jumbo_inner(categ_id)
		
# --------4 Disco Product Scrape
def scrape_product_disco(url):
	driver.get(url)
	categories = db.get_category('4')
	for category in categories:
		sleep(5)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(category[1]))
		sleep(5)
		product_content = driver.find_elements_by_xpath('//*[@id="product-list"]/child::li')
		for i in range(0,len(product_content)):
			try:
				image = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-imagen"]/img[@class="centered-image small lazy"]').get_attribute('src')
				price = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-precio"]').get_attribute('textContent').strip()
				try:
					tail = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-precio"]/span').get_attribute('textContent').strip()
					price = price.split(str(tail))[0] + '.' + tail
				except:
					price = price
				name = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-descripcion"]').get_attribute('textContent').strip()
				discount = ''
				product.append((image, name, price, discount, category[0]))
			except:
				continue
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]

# --------5 Coto Product Scrape
def scrape_coto_page(categ_id):
	page_content = driver.find_elements_by_xpath('//*[@id="products"]/child::li')
	print(len(page_content))
	for i in range(0, len(page_content)):
		try:
			image = driver.find_element_by_xpath('//*[@id="products"]/child::li[' + str(i + 1) + ']/div[1]/div/a/span[1]/img').get_attribute('src')
			name = driver.find_element_by_xpath('//*[@id="products"]/child::li[' + str(i + 1) + ']/div[1]/div/a/span[2]/div/span/div/div').get_attribute('textContent').strip()
			price = ''
			try:
				price = driver.find_element_by_xpath('//*[@id="products"]/child::li[' + str(i + 1) + ']/div[2]/div[1]/div[1]/div/div/div[1]/span[2]').text.strip()
			except:
				try:
					price = driver.find_element_by_xpath('//*[@id="products"]/child::li[' + str(i + 1) + ']/div[2]/div[1]/div[1]/span/span').text.strip().split('PRECIO CONTADO')[1]
				except:
					price = ''
			product.append((image, name, price, '', categ_id))
		except:
			continue

def get_coto_product(index, id):
	scrape_coto_page(id)
	pagination = driver.find_elements_by_xpath('//*[@id="atg_store_pagination"]/child::li')
	for item in pagination:
		try:
			item_txt = item.find_element_by_tag_name('a').get_attribute('textContent').strip()
			if item_txt == str(index + 1):
				index += 1
				item.click()
				get_coto_product(index, id)
		except:
			print('no text!')

def scrape_product_coto():
	categories = db.get_category('5')
	for category in categories:
		url = category[1]
		driver.get(url)
		id = category[0]
		get_coto_product(1, id)
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]

# --------6 Carrefour Product Scrape
def scrape_product_carrefour():
	categories = db.get_category('6')
	for category in categories:
		driver.get(category[1])
		sleep(5)
		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			new_height = driver.execute_script('return document.body.scrollHeight')
			sleep(5)
			if new_height == last_height:
				try:
					viewmore = driver.find_element_by_class_name('ver-mas-productos')
					print(viewmore.value_of_css_property("display"))
					if viewmore.value_of_css_property("display") != "none":
						driver.execute_script("arguments[0].click();", viewmore)
						sleep(5)
					else:
						break
				except:
					print("viewmore not found!")
			last_height = new_height
			print('---End---')
		product_content = driver.find_elements_by_xpath('//div[@class="category-products"]/div[2]/div[@class="row"]/child::div')
		for i in range(0, len(product_content)):
			try:
				image = driver.find_element_by_xpath('//div[@class="category-products"]/div[2]/div[@class="row"]/child::div[' + str(i + 1) + ']/div/div[@class="image"]/a/img').get_attribute('src')
				price = driver.find_element_by_xpath('//div[@class="category-products"]/div[2]/div[@class="row"]/child::div[' + str(i + 1) + ']/div/div[@class="producto-info"]/a/div[2]/p[1]').get_attribute('textContent').strip()
				name = driver.find_element_by_xpath('//div[@class="category-products"]/div[2]/div[@class="row"]/child::div[' + str(i + 1) + ']/div/div[@class="producto-info"]/a/p[@class="title title-food truncate"]').get_attribute('textContent').strip()
				discount = ''
				product.append((image, name, price, discount, category[0]))
			except:
				continue
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]
# --------7 Vea Product Scrape
def scrape_product_vea(url):
	driver.get(url)
	categories = db.get_category('7')
	for category in categories:
		sleep(5)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(category[1]))
		sleep(5)
		product_content = driver.find_elements_by_xpath('//*[@id="product-list"]/child::li')
		for i in range(0,len(product_content)):
			try:
				image = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-imagen"]/img[@class="centered-image small lazy"]').get_attribute('src')
				price = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-precio"]').get_attribute('textContent').strip()
				try:
					tail = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-precio"]/span').get_attribute('textContent').strip()
					price = price.split(str(tail))[0] + '.' + tail
				except:
					price = price
				name = driver.find_element_by_xpath('//*[@id="product-list"]/child::li['+ str(i+1) +']/div[@class="grilla-producto fluid-grid-item "]/div[1]/div[@class="grilla-producto-informacion"]/div/div[@class="grilla-producto-descripcion"]').get_attribute('textContent').strip()
				discount = ''
				product.append((image, name, price, discount, category[0]))
			except:
				continue
		db.insert_data("tbl_products", "image, product, price, discount, category","%s,%s,%s,%s,%s", product)
		del product[:]

# --------1 Dia Discount
def scrape_discount_dia(url):
	discount = []
	driver.get(url)
	mon_content = driver.find_elements_by_xpath('//div[@id="todos-los-lunes"]/div/child::div[@class="promos-box"]')
	for monday in mon_content:
		supermarket = 1
		day = 1
		logo = monday.find_element_by_xpath('//div[@class="wysiwyg contenido"]').find_elements_by_tag_name('p')[1].find_element_by_tag_name('img').get_attribute('src')
		disc = monday.find_elements_by_tag_name('h2')[0].get_attribute('textContent')
		print(disc)
		description = monday.find_element_by_class_name('descripcion').get_attribute('textContent')
		driver.execute_script("arguments[0].click();", monday.find_element_by_class_name('ver_legales'))
		sleep(2)
		more = driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('modal-content').find_element_by_class_name('modal-body').get_attribute('textContent').replace('&nbsp;','').strip()
		print(more)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('close'))
		sleep(2)
		discount.append((supermarket, day, logo, disc, description, more))
	wed_content = driver.find_elements_by_xpath('//div[@id="todos-los-miercoles"]/div/child::div[@class="promos-box"]')
	for wednesday in wed_content:
		supermarket = 1
		day = 3
		logo = wednesday.find_element_by_xpath('//div[@class="wysiwyg contenido"]').find_elements_by_tag_name('p')[1].find_element_by_tag_name('img').get_attribute('src')
		disc = wednesday.find_elements_by_tag_name('h2')[0].get_attribute('textContent')
		description = wednesday.find_element_by_class_name('descripcion').get_attribute('textContent')
		driver.execute_script("arguments[0].click();", wednesday.find_element_by_class_name('ver_legales'))
		more = driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('modal-content').find_element_by_class_name('modal-body').get_attribute('textContent').replace('&nbsp;','').strip()
		sleep(2)
		print(more)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('close'))
		sleep(2)
		discount.append((supermarket, day, logo, disc, description, more))
	every_content = driver.find_elements_by_xpath('//div[@id="todos-los-dias"]/div/child::div[@class="promos-box"]')
	for every in every_content:
		supermarket = 1
		day = 0
		logo = every.find_element_by_xpath('//div[@class="wysiwyg contenido"]').find_elements_by_tag_name('p')[1].find_element_by_tag_name('img').get_attribute('src')
		disc = every.find_elements_by_tag_name('h2')[0].get_attribute('textContent')
		description = every.find_element_by_class_name('descripcion').get_attribute('textContent')
		driver.execute_script("arguments[0].click();", every.find_element_by_class_name('ver_legales'))
		more = driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('modal-content').find_element_by_class_name('modal-body').get_attribute('textContent').replace('&nbsp;','').strip()
		sleep(2)
		print(more)
		driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//div[@class="modal fade show"]').find_element_by_class_name('close'))
		sleep(2)
		discount.append((supermarket, day, logo, disc, description, more))
	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)

# --------2 Walmart Discount
def scrape_discount_walmart(url):
	discount = []
	list_content = [[8,'https://cdn140.picsart.com/286371110019211.png?type=webp&to=min&r=640','HASTA 6 CUOTAS FIJAS','HASTA 6 CUOTAS FIJAS','Recordá que los pagos online se realizan a través de Mercado Pago. Los planes de cuotas serán los ofrecidos por Mercado Pago.']
					,[8,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','20%','En un pago','Válido por 4 transacciones por cuenta y por mes calendario. Tope $500 por transacción. No incluye electro. Ver legales al final de esta página.']
					,[3,'https://estaciondelsiglo.net/wp-content/uploads/2020/03/1200px-Logo_Banco_Macro.svg_.png','20%','Con tarjeta de crédito','Válido en un pago. Tope de reintegro $800 por mes por cuenta. No incluye electro. Aplica a las tarjetas: MasterCard Black, MasterCard Gold, MasterCard Internacional, MasterCard Platinum, Visa Gold, Visa Internacional, Visa Platinum, Visa Signature, Visa Bussiness. Ver legales al final de esta página.']
					,[8,'https://i.pinimg.com/originals/4c/3a/56/4c3a561a9e1b2819174bdc011d3ac026.png','20%','Tope: $350','No incluye electro. Aplica a las tarjetas Visa con adquirencia Prisma.']
					,[8,'https://i.pinimg.com/originals/4c/3a/56/4c3a561a9e1b2819174bdc011d3ac026.png','30%','Canjeando 5.000 puntos. Tope: $500','No incluye electro. Aplica a las tarjetas Visa con adquirencia Prisma.']
					,[8,'https://i.pinimg.com/originals/4c/3a/56/4c3a561a9e1b2819174bdc011d3ac026.png','40%','Canjeando 7.000 puntos. Tope: $800','No incluye electro. Aplica a las tarjetas Visa con adquirencia Prisma.']
					,[8,'http://www.opticadontorcuato.com.ar/images/client_gallery/Promociones_archivos/image006.jpg','10%','Canjeando 300 puntos. Tope: $300','Válido para tarjetas Galicia VISA, Galicia MasterCard, Galicia American Express y Galicia Débito. Ver legales al final de esta página.']
					,[8,'http://www.opticadontorcuato.com.ar/images/client_gallery/Promociones_archivos/image006.jpg','20%','Canjeando 500 puntos. Tope: $600','Válido para tarjetas Galicia VISA, Galicia MasterCard, Galicia American Express y Galicia Débito. Ver legales al final de esta página.']
					,[8,'https://paymentweek.com/wp-content/uploads/2017/11/Logotipo_del_Banco_Santander-1024x592.jpg','10%','Canjeando 2.900 puntos. Tope: $250','Válido para tarjeta Santander Crédito del titular o sus adicionales, o Débito del titular que haya efectuado el canje. Excluye Electro. Ver legales al final de esta página.']
					,[8,'https://paymentweek.com/wp-content/uploads/2017/11/Logotipo_del_Banco_Santander-1024x592.jpg','20%','Canjeando 5.500 puntos. Tope: $500','Válido para tarjeta Santander Crédito del titular o sus adicionales, o Débito del titular que haya efectuado el canje. Excluye Electro. Ver legales al final de esta página.']
					,[8,'https://paymentweek.com/wp-content/uploads/2017/11/Logotipo_del_Banco_Santander-1024x592.jpg','30%','Canjeando 8.000 puntos. Tope: $650','Válido para tarjeta Santander Crédito del titular o sus adicionales, o Débito del titular que haya efectuado el canje. Excluye Electro. Ver legales al final de esta página.']
					,[8,'https://paymentweek.com/wp-content/uploads/2017/11/Logotipo_del_Banco_Santander-1024x592.jpg','40%','Canjeando 10.000 puntos. Tope: $1500','Válido para tarjeta Santander Crédito del titular o sus adicionales, o Débito del titular que haya efectuado el canje. Excluye Electro. Ver legales al final de esta página.']
					,[3,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','15%','','Válido en un pago. No incluye electro. Tope de reintegro $500 por transacción (hasta 4 transacciones por mes). El reintegro se verá reflejado en el resumen. Ver legales al final de esta página.']
					,[4,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','3 CUOTAS SIN INTERÉS','En toda tu compra','No incluye electro. Ver legales al final de esta página.']
					,[5,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','3 CUOTAS SIN INTERÉS','En toda tu compra','No incluye electro. Ver legales al final de esta página.']
					,[6,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','3 CUOTAS SIN INTERÉS','En toda tu compra','No incluye electro. Ver legales al final de esta página.']
					,[7,'https://storage3.embluemail.com/clientes/plataforma10/2017/Enero/2701/walmart_mastercard.jpg','3 CUOTAS SIN INTERÉS','En toda tu compra','No incluye electro. Ver legales al final de esta página.']
					,[8,'https://www.seekpng.com/png/full/46-468769_solucionado-reclamo-a-naranja-logo-tarjeta-naranja-png.png','3 CUOTAS SIN INTERÉS','Con Plan Zeta','No incluye electro. Ver legales al final de esta página.']
					,[8,'https://www.kindpng.com/picc/m/35-351793_credit-or-debit-card-mastercard-logo-visa-card.png','4 CUOTAS SIN INTERÉS','','Válido únicamente con la TARJETA CORDOBESA MASTERCARD o TARJETA CORDOBESA VISA. Ver legales al final de esta página.']
					,[1,'https://agenfor.com.ar/wp-content/uploads/2019/09/unnamed-1.jpg','15%','Con tarjeta de débito','Tope $300 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'https://getvectorlogo.com/wp-content/uploads/2018/12/banco-hipotecario-vector-logo.png','25%','Con tarjeta de débito','Tope $1500 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'http://www.ceer.org/wp-content/uploads/2015/05/Banco_NB.jpg','15%','Con tarjeta de crédito','Tope $600 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'https://rufinoweb.com.ar/wp-content/uploads/2018/12/banco-santa-fe-1024x597.png','15%','Con tarjeta de crédito','Tope $600 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'https://tuquejasuma.com/media/cache/8c/f7/8cf74e9cddb6ed2d787527641bceffd3.jpg','15%','Con tarjeta de crédito','Tope $600 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'https://pbs.twimg.com/profile_images/928276722776268802/Kp6EsiWN_400x400.jpg','15%','','Tope $400 por mes. No incluye electro. Ver legales al final de esta página.']
					,[2,'https://www.kindpng.com/picc/m/393-3934257_banco-supervielle-logo-png-transparent-png.png','15%','Con tarjeta de débito','Tope de reintegro $1000 por cuenta por mes. No incluye electro. Ver legales al final de esta página.']
					,[3,'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Banco_Naci%C3%B3n.svg/210px-Banco_Naci%C3%B3n.svg.png','20%','Con tarjeta de crédito','Válido en un pago. Tope de reintegro $1200 en la primera transacción realizada en alguno de los locales adheridos a la promoción. No incluye electro ni carne vacuna. Ver legales al final de esta página.']
					,[3,'https://cincosolesturismo.com/wp-content/uploads/2017/12/banco-corrientes.jpg','10%','Con tarjeta de débito','Sin tope de reintegro. No incluye electro. Ver legales al final de esta página.']
					,[5,'https://oblyo.ro/wp-content/uploads/2019/04/Logo-Unica.ro_.png','10%','Con tarjeta de débito','Válido en un pago. Sin tope de reintegro. Ver legales al final de esta página.']]
	print(len(list_content))

	for i in range(len(list_content)):
		supermarket = 2
		day = list_content[i][0]
		logo = list_content[i][1]
		disc = list_content[i][2]
		description = list_content[i][3]
		more = list_content[i][4]
		discount.append((supermarket, day, logo, disc, description, more))

	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]

# --------3 Jumbo Discount
def scrape_discount_jumbo(url):
	discount = []
	for i in range(len(url)):
		driver.get(url[i])
		list_content = driver.find_elements_by_xpath('//div[@class="discounts__list"]/div/child::div')
		for item in list_content:
			supermarket = 3
			day = i + 1
			logo = ''
			try:
				logo = item.find_element_by_class_name('discounts__item-bank').find_element_by_tag_name('img').get_attribute('src')
			except:
				logo = 'http://abappra.com.ar/imgdb/logos_bancos/internas/e7-banco_nacion.png'
			disc = item.find_element_by_class_name('discounts__item-data').get_attribute('textContent').split('Dto')[0].strip()
			print(disc)
			description = item.find_element_by_class_name('discounts__item-info').get_attribute('textContent').strip()
			driver.execute_script("arguments[0].click();", item.find_element_by_tag_name('button'))
			sleep(1)
			more = item.find_element_by_class_name('discounts__item-legals').get_attribute('textContent').strip()
			discount.append((supermarket, day, logo, disc, description, more))
	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]

# --------4 Disco Discount
def scrape_discount_disco(url):
	discount = []
	driver.get(url)
	for i in range(7):
		list_content = driver.find_elements_by_xpath('//div[@id="promociones"]/div/child::div')
		for item in list_content:
			supermarket = 4
			day = i + 1
			logo = item.find_element_by_class_name('promo_logo-bank').find_element_by_tag_name('img').get_attribute('src')
			disc = item.find_element_by_class_name('promo_dto-porcent').get_attribute('textContent').strip()
			print(disc)
			description = item.find_element_by_class_name('promo_dto').get_attribute('textContent').split('%')[1].strip() + " " + item.find_element_by_class_name('promo_info').get_attribute('textContent')
			driver.execute_script("arguments[0].click();", item.find_element_by_class_name('promo_verMas'))
			sleep(1)
			more = item.find_element_by_class_name('dropdown_detalles-legal').get_attribute('textContent').strip()
			discount.append((supermarket, day, logo, disc, description, more))
	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]

# --------5 Coto Discount
def scrape_discount_coto(url):
	discount = []
	driver.get(url)
	list_theme = driver.find_elements_by_xpath('//*[@id="day_div"]/ul/child::li')
	for i in range(len(list_theme)):
		try:
			driver.execute_script("arguments[0].click();", list_theme[i])
			sleep(1)
			list_content = driver.find_elements_by_xpath('//*[@id="Grid"]/child::li')
			print(len(list_content))
			
			for item in list_content:
				try:
					val = item.value_of_css_property("opacity")
					if val == "1":
						supermarket = 5
						day = i + 1
						logo = ""
						try:
							logo = "https://www.coto.com.ar/descuentos/"+item.find_element_by_class_name('desc_bank_img').find_element_by_tag_name('img').get_attribute('src')
						except:
							print("no payment!")
						disc = item.find_element_by_class_name('desc_numero').find_element_by_tag_name('img').get_attribute('alt').split('descuento')[0].split('ahorro')[0].strip()
						description = item.find_element_by_class_name('desc_info').get_attribute('textContent').strip()
						print(disc)
						more = item.find_element_by_class_name('desc_info_condiciones').get_attribute('textContent').strip()
						discount.append((supermarket, day, logo, disc, description, more))
				except:
					print("no element!")
		except:
			print("total error!")
	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]

# --------6 Carrefour Discount
def scrape_discount_carrefour(url):
	discount = []
	driver.get(url)

	list_content = driver.find_elements_by_xpath('//*[@id="promolanding-wrapper"]/div[12]/div/child::div')

	for i in range(len(list_content)):
		try:
			supermarket = 6
			day = list_content[i].find_element_by_class_name('benefit-rest-day').get_attribute('textContent').strip()
			if day == "MARTES":
				day = 2
			elif day == "MIÉRCOLES":
				day = 3
			elif day == "TODOS LOS DÍAS":
				day = 8	
			logo = list_content[i].find_element_by_class_name('benefit-rest-image').find_element_by_tag_name('img').get_attribute('src')
			disc = list_content[i].find_element_by_class_name('benefit-rest-title').get_attribute('textContent').split('DE DESCUENTO')[0].strip()
			description = list_content[i].find_element_by_class_name('benefit-rest-tex-alternative').get_attribute('textContent').strip()
			print(disc)
			more = description
			discount.append((supermarket, day, logo, disc, description, more))
		except:
			print("no element!")

	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]

# --------7 Vea Discount
def scrape_discount_vea(url):
	discount = []
	driver.get(url)
	for i in range(7):
		list_content = driver.find_elements_by_xpath('//div[@id="promociones"]/div/child::div')
		for item in list_content:
			supermarket = 7
			day = i + 1
			logo = item.find_element_by_class_name('promo_logo-bank').find_element_by_tag_name('img').get_attribute('src')
			disc = item.find_element_by_class_name('promo_dto-porcent').get_attribute('textContent').strip()
			print(disc)
			description = item.find_element_by_class_name('promo_dto').get_attribute('textContent').split('%')[1].strip() + " " + item.find_element_by_class_name('promo_info').get_attribute('textContent')
			driver.execute_script("arguments[0].click();", item.find_element_by_class_name('promo_verMas'))
			sleep(1)
			more = item.find_element_by_class_name('dropdown_detalles-legal').get_attribute('textContent').strip()
			discount.append((supermarket, day, logo, disc, description, more))
	db.insert_data("tbl_discount", "supermarket, day, payment_type, discount, description, more","%s,%s,%s,%s,%s,%s", discount)
	del discount[:]


# ----- Argentina Supermarkets -----------
url_categ_dia = 'https://diaonline.supermercadosdia.com.ar/'
url_categ_walmart = 'https://www.walmart.com.ar/'
url_categ_jumbo = 'https://www.jumbo.com.ar/'
url_categ_disco = 'https://www.disco.com.ar/Comprar/Home.aspx#_atCategory=false&_atGrilla=true&_id=446242'
url_categ_coto = 'https://www.cotodigital3.com.ar/sitios/cdigi/browse?_dyncharset=utf-8&Dy=1&Nty=1&Ntk=All%7Cproduct.s'
url_categ_carrefour = 'https://supermercado.carrefour.com.ar/'
url_categ_vea = 'https://www.veadigital.com.ar/'

# -----Discount URLs
url_product_dia = 'https://www.supermercadosdia.com.ar/medios-de-pago-y-promociones/'
url_product_walmart = 'https://www.walmart.com.ar/medios-de-pago?gclid=Cj0KCQjw-Mr0BRDyARIsAKEFbecrTxM_c-h76KMW_GxpKYrz_RW0EOkLZewp-HdV_2T_BG8veySFvnIaAtHrEALw_wcB'
url_product_jumbo = ['https://www.jumbo.com.ar/descuentos?dia-lunes', 'https://www.jumbo.com.ar/descuentos?dia-martes', 'https://www.jumbo.com.ar/descuentos?dia-miercoles', 'https://www.jumbo.com.ar/descuentos?dia-jueves', 'https://www.jumbo.com.ar/descuentos?dia-viernes', 'https://www.jumbo.com.ar/descuentos?dia-sabado']
url_product_disco = 'https://www.disco.com.ar/Descuentos/Descuentos.aspx'
url_product_coto = 'https://www.coto.com.ar/descuentos/'
url_product_carrefour = 'https://www.carrefour.com.ar/promociones'
url_product_vea = 'https://www.veadigital.com.ar/Descuentos/Descuentos.aspx'

scrape_categ_dia(url_categ_dia)
scrape_categ_walmart(url_categ_walmart)
scrape_categ_jumbo(url_categ_jumbo)
scrape_categ_disco(url_categ_disco)
scrape_categ_coto(url_categ_coto)
scrape_categ_carrefour(url_categ_carrefour)
scrape_categ_vea(url_categ_vea)

scrape_product_dia()
scrape_product_walmart()
scrape_product_jumbo()
scrape_product_disco(url_categ_disco)
scrape_product_coto()
scrape_product_carrefour()
scrape_product_vea(url_categ_vea)

scrape_discount_dia(url_product_dia)
scrape_discount_walmart(url_product_walmart)
scrape_discount_jumbo(url_product_jumbo)
scrape_discount_disco(url_product_disco)
scrape_discount_coto(url_product_coto)
scrape_discount_carrefour(url_product_carrefour)
scrape_discount_vea(url_product_vea)

sleep(3)
driver.quit()
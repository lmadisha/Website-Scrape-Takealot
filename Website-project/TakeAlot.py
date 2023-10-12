from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import lxml
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.takealot.com/")

search = driver.find_element(By.XPATH, '//*[@id="shopfront-app"]/header/div/div/div[2]/form/div[1]/div[1]/input')
name_product = input('Enter a product or service: ')
search.send_keys(name_product)
search.send_keys(Keys.ENTER)
time.sleep(5)

list_of_items = driver.find_elements(By.CSS_SELECTOR, 'div.search-product.grid a')

items_link = []

for a in list_of_items:
    items_link.append(a.get_property('href'))

items_links = []

for link in items_link:
    if 'filter' not in link:
        items_links.append(link)

links = list(OrderedDict.fromkeys(items_links))

driver.close()

information = []

for l in links:
    driver1 = webdriver.Chrome(options=chrome_options)
    driver1.get(l)
    time.sleep(5)
    name = driver1.find_element(By.CSS_SELECTOR, "div.product-title h1").text
    price = driver1.find_element(By.CSS_SELECTOR, 'div.buybox-module_price_2YUFa span').text

    # descriptions = driver1.find_elements(By.CSS_SELECTOR, 'div.product-description p')
    # description = []
    # for x in descriptions:
    #     description.append(x.text)
    # description = description[1:]

    table = driver1.find_element(By.CSS_SELECTOR, 'div.product-info table')
    time.sleep(5)
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "lxml")
    table_data = []
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        table_data.append(output_row)
    barcode = table_data[len(table_data)-1][1]
    product_info = table_data

    info_dic = {
        'Name': name,
        'Price': price,
        'Barcode': barcode,
        'Link': l,
        'Product Information': product_info,
    }

    information.append(info_dic)

    driver1.close()

fields = ['Name', 'Price', 'Barcode', 'Link', 'Product Information']
filename = f"{name_product}.csv"

with open(filename, "wt") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(information)

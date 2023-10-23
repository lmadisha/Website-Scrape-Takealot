from collections import OrderedDict

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import lxml
import csv

# <--------------------------------------------Setting up webdriver ------------------------------------------------------------->

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.takealot.com/")

#<--------------------------------------------- Searching up the product-------------------------------------------------------->

search = driver.find_element(By.XPATH, '//*[@id="shopfront-app"]/header/div/div/div[2]/form/div[1]/div[1]/input')
name_product = input('Enter a product or service: ')
search.send_keys(name_product)
search.send_keys(Keys.ENTER)
time.sleep(5)

#<--------------------------------------------- Getting all the products links--------------------------------------------------->

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

#<--------------------------------------------- Getting all the information of the products----------------------------------------->

information = []

driver1 = webdriver.Chrome(options=chrome_options)

for l in links:
    driver1.get(l)
    time.sleep(3)
    name = driver1.find_element(By.CSS_SELECTOR, "div.product-title h1").text
    price = driver1.find_element(By.CSS_SELECTOR, 'span.currency.plus.currency-module_currency_29IIm').text

    # price = float((price[2:]).replace(",", ""))

    # descriptions = driver1.find_elements(By.CSS_SELECTOR, 'div.product-description p')
    # description = []
    # for x in descriptions:
    #     description.append(x.text)
    # description = description[1:]

    try:
        table = driver1.find_element(By.CSS_SELECTOR, 'div.product-info table')
        time.sleep(2.5)
    except selenium.common.exceptions.NoSuchElementException:
        barcode = 'No barcode'
        product_info = 'No product information yet!!'
    else:
        soup = BeautifulSoup(table.get_attribute('outerHTML'), "lxml")
        table_data = []
        time.sleep(2.5)
        for row in soup.find_all('tr'):
            columns = row.find_all('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            table_data.append(output_row)

        if (table_data[len(table_data) - 1][0]) == 'Barcode':
            barcode = table_data[len(table_data) - 1][1]
        else:
            barcode = 'No barcode'

        product_info = table_data

    info_dic = {
        'Name': name,
        'Price': float((price[2:]).replace(",", "")),
        'Barcode': barcode,
        'Link': l,
        'Product Information': product_info,
    }

    information.append(info_dic)

driver1.close()

#<--------------------------------------------- CSV ------------------------------------------------------------------------------>
# import pandas as pandasForSortingCSV


fields = ['Name', 'Price', 'Barcode', 'Link', 'Product Information']
filename = f"{name_product}.csv"

information_dict = sorted(information, key=lambda x: x['Price'])
# print(information_dict)

with open(filename, "wt") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(information_dict)

# csvData = pandasForSortingCSV.read_csv(filename)
# csvData.sort_values(["Price"],
#                     axis=0,
#                     ascending=[True],
#                     inplace=True)
#
# print(csvData['Name']['Price'])
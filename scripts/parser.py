import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scripts.utils.xpath_constants import (DICT_CITY_XPATH,
                                           PRODUCT_CARD_XPATH,
                                           CARD_URL_XPATH,
                                           ACTUAL_PRICE_XPATH,
                                           DISCOUNT_PRICE_XPATH,
                                           ACTUAL_PRICE_PENNY_XPATH,
                                           DISCOUNT_PRICE_PENNY_XPATH)

SITE_URL = "https://online.metro-cc.ru"
TARGET_URL = "/category/bezalkogolnye-napitki/pityevaya-voda-kulery?in_stock=1"


class ParserMetro:

    def __init__(self, site_url, category_url, target_city):
        self.site_url = site_url
        self.category_url = category_url
        self.target_city = target_city
        self.xpath_city = DICT_CITY_XPATH.get(target_city)
        self.driver = webdriver.Chrome()

    def __change_city(self):
        self.driver.get(self.site_url + self.category_url)

        select_city_button = self.driver.find_element(By.CSS_SELECTOR, '.select-button')

        self.driver.execute_script("arguments[0].click();", select_city_button)
        city_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.xpath_city))
        )
        self.driver.execute_script("arguments[0].click();", city_element)

    def __get_url_cards(self):
        self.__change_city()
        for count in range(1, 10):
            url = self.site_url + self.category_url + f'&page={count}'
            self.driver.get(url)
            product_cards = self.driver.find_elements(By.XPATH, PRODUCT_CARD_XPATH)

            for product_card in product_cards:
                card_url = product_card.find_element(By.XPATH, CARD_URL_XPATH).get_attribute('href')
                actual_price_rubles = product_card.find_element(By.XPATH, ACTUAL_PRICE_XPATH)
                try:
                    discount_price_rubles = product_card.find_element(By.XPATH, DISCOUNT_PRICE_XPATH)
                except NoSuchElementException:
                    discount_price_rubles = None
                if actual_price_rubles and discount_price_rubles:
                    promo_price = actual_price_rubles.text.strip().replace(' ', '')
                    price = discount_price_rubles.text.strip().replace(' ', '')
                    try:
                        actual_price_penny = product_card.find_element(By.XPATH, ACTUAL_PRICE_PENNY_XPATH)
                        promo_price = float(promo_price + actual_price_penny.text.strip())
                    except NoSuchElementException:
                        promo_price = float(promo_price)
                    try:
                        discount_price_penny = product_card.find_element(By.XPATH, DISCOUNT_PRICE_PENNY_XPATH)
                        price = float(price + discount_price_penny.text.strip())
                    except NoSuchElementException:
                        price = float(price)
                else:
                    price = actual_price_rubles.text.strip().replace(' ', '')
                    promo_price = None
                    try:
                        actual_price_penny = product_card.find_element(By.XPATH, ACTUAL_PRICE_PENNY_XPATH)
                        price = float(price + actual_price_penny.text.strip())
                    except NoSuchElementException:
                        price = float(price)
                yield {'card_url': card_url, 'price': price, 'promo_price': promo_price}

    def __get_product_info(self):
        for product in self.__get_url_cards():
            card_url = product.get('card_url')
            response = requests.get(card_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                price = product.get('price')
                promo_price = product.get('promo_price')
                name = soup.find('h1', class_='product-page-content__product-name').find('span').text.strip()
                articul = int(soup.find('p', {'itemprop': 'productID'}).text.strip().split(":")[-1].strip())
                url_product = card_url
                brand = soup.find('a',
                                  class_='product-attributes__list-item-link reset-link active-blue-text').text.strip()
                yield {'articul': articul,
                       'name': name,
                       'url_product': url_product,
                       'brand': brand,
                       'price': price,
                       'promo_price': promo_price
                       }

    def analyze_products(self):
        with open(f'../data/report{self.target_city}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Articul', 'Name', 'URL', 'Price', 'Promo Price', 'Brand']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product_info in self.__get_product_info():
                writer.writerow({'Articul': product_info.get('articul'),
                                 'Name': product_info.get('name'),
                                 'URL': product_info.get('url_product'),
                                 'Price': product_info.get('price'),
                                 'Promo Price': product_info.get('promo_price'),
                                 'Brand': product_info.get('brand'),
                                 })


if __name__ == "__main__":
    parser_msk = ParserMetro(SITE_URL, TARGET_URL, 'MSK')
    parser_msk.analyze_products()
    parser_msk.driver.quit()
    parser_spb = ParserMetro(SITE_URL, TARGET_URL, 'SPB')
    parser_spb.analyze_products()
    parser_spb.driver.quit()

DICT_CITY_XPATH = {
    'SPB': '//span[contains(text(), "Санкт-Петербург")]',
    'MSK': '//span[contains(text(), "Москва")]',
}

PRODUCT_CARD_XPATH = "//div[contains(@class, 'catalog-2-level-product-card product-card')]"

CARD_URL_XPATH = ".//a[@data-qa='product-card-name']"
ACTUAL_PRICE_XPATH = ".//div[@class='product-unit-prices__actual-wrapper']//span[@class='product-price__sum-rubles']"
DISCOUNT_PRICE_XPATH = ".//div[@class='product-unit-prices__old-wrapper']//span[@class='product-price__sum-rubles']"
ACTUAL_PRICE_PENNY_XPATH = ".//div[@class='product-unit-prices__actual-wrapper']//span[@class='product-price__sum-penny']"
DISCOUNT_PRICE_PENNY_XPATH = ".//div[@class='product-unit-prices__old-wrapper']//span[@class='product-price__sum-penny']"

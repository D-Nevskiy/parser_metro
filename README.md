# Парсер для сайта Metro

 💻 Парсер собирает информацию товаров из категории "Вода" в городе Москва и Санкт-Петербург и формирует csv файл с отчетом.

Данные:
- id товара из сайта/приложения, 
- наименование, 
- ссылка на товар, 
- регулярная цена, 
- промо цена, 
- бренд.

## Порядок установки и запуска приложения на localhost

- Установите и активируйте виртуальное окружение
```
# Windows:
python -m venv venv
source venv/Scripts/activate 
# MacOS или Linux:
python3 -m venv venv
source venv/bin/activate 
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Запуск скрипта
```
python parser.py
```
- [ChromeDriver v.119.0.6045.105](https://googlechromelabs.github.io/chrome-for-testing/#stable) Распакуйте архив и поместите `chromedriver` в корень проекта
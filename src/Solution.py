import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


# ------------------------------------------------------STEP 1------------------------------------------------------------
# Допустим мы выгрузили из БД все url-страницы в один Excel файл (URL.xlsx)

# ------------------------------------------------------STEP 2------------------------------------------------------------

file_path = "../../URL.xlsx"  # Путь до Excel файла с URL-адресами

# Считывание URL из Excel файла и добавление их в список urls
def read_urls_from_excel(file_path):
    urls = []
    df = pd.read_excel(file_path)
    for url in df['URL_PAGE']:
        urls.append(url)
    return urls

# ------------------------------------------------------STEP 3------------------------------------------------------------
# Сохраним Web-страницы (.html) в локальной папке проекта "downloaded_pages"
def download_web_pages(url_list):
    url_list = read_urls_from_excel(file_path)
    
    header = {
    "Accept": "text/html,....................",
    "User-Agent": ".........................."
    }

    count = 1
    for i in url_list:
        response = requests.get(i, headers=header)
        src = response.content
        with open(f"downloaded_pages/web_page_{count}.html", "wb") as file:
            file.write(src)
        count += 1

    return print("\nWeb-pages saved successfully!")


# ------------------------------------------------------STEP 4------------------------------------------------------------
# Метод для расчета количества url страниц в excel файле
def url_page_count(file_path):
    url_list = read_urls_from_excel(file_path)
    return len(url_list)

# Далее работаем уже с сохраненными web-страницами
# Метод для поиска номеров на web-странице
# Входные данные: путь, где хранится URL.xlsx
# Выходные данные: множество с необходимыми телефонами
def find_phone_numbers(file_path):

    last_page = url_page_count(file_path)

    for i in range(1, last_page + 1):
        with open(f"downloaded_pages/web_page_{i}.html") as file:
            url = file.read()
    
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
    
        phone_numbers = set()
        pattern = re.compile(r'8\d{10}')  # Паттерн для нахождения российских номеров телефонов
    
        for script in soup(['script', 'style']):
            script.extract()  # Удаляем все скрипты и стили из HTML
    
        text = soup.get_text()
        numbers_found = pattern.findall(text)
    
        for number in numbers_found:
            if len(number) == 11:  # Проверяем, что номер имеет код города
                phone_numbers.add(number)
            else:
                # Добавляем код города Москвы (495) к номеру, если код не указан
                moscow_number = '8495' + number[1:]
                phone_numbers.add(moscow_number)

    print("\nSuccessfully parsed!")
    return phone_numbers

# ------------------------------------------------------STEP 5------------------------------------------------------------
# Вывод результата и сохранение данных в Excel
res_phone_numbers = find_phone_numbers(file_path)

for phone_number in res_phone_numbers:
    print(phone_number)

phone_numbers_df = pd.DataFrame(res_phone_numbers, columns=["Phone_Number"])

# Сохранение DataFrame в Excel файл
phone_numbers_df.to_excel("phone_numbers.xlsx", index=False)

# Результат работы программы будет выведен на экран и сохранен в Excel файл "phone_numbers.xlsx"




import time
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
以下是
(1) 在SSR的情況下，直接使用requests去抓html的資料
(2) 在CSR的情況下，需搭配selenium自動化瀏覽去loading data，在使用requests獲取資料

'''

# for i in range(4):
#     print(f'====第{i}頁====')
#     url = f'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p={i}'
#     response = requests.get(url)
#     html = response.text

#     soup = BeautifulSoup(html, 'html.parser')
#     sections = soup.find_all('section', {'class': 'infoArea'})

#     for sec in sections:
#         print(sec.find('a').text)


# 以下是一個儲存圖片的示範
driver = webdriver.Chrome()
driver.get("https://uma.komoejoy.com/character.html")
html = driver.page_source
# print(html)

soup = BeautifulSoup(html, 'html.parser')
imgs = soup.find_all('img')

for img in imgs:
    try:
        url = 'http:' + img['data-src']
        name = img['alt']
        resp = requests.get(url)
        img = resp.content
        os.makedirs('test', exist_ok=True)
        with open(f'test/{name}.png', 'wb') as f:
            f.write(img)
    except:
        pass

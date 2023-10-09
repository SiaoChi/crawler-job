import datetime
import time
import requests
import os
import csv
from bs4 import BeautifulSoup

urls = [
    f'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&kwop=7&keyword=Node.js%20JavaScript&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=12&asc=0&page=2&jobexp=1%2C3&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
    f'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&keyword=python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=1&asc=0&page=1&jobexp=1%2C3&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
    f'https://www.104.com.tw/jobs/search/?ro=0&isnew=0&kwop=7&keyword=%E5%BE%8C%E7%AB%AF&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob'
    f'https://www.104.com.tw/jobs/search/?ro=0&isnew=0&keyword=%E8%BB%9F%E9%AB%94%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001002000%2C6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob'
]

pages = 3

for url in urls:
    for p in range(pages):
        print(f'===== 第{p}頁 =====')
        requestURL = f'{url}={p}'
        res = requests.get(requestURL)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        print(current_datetime_str)
        jobs = soup.find_all('article', {'class': 'job-list-item'})

        if not jobs:
            p = 0
            print('=== 頁面無資料 ===')
            break

        for i in range(len(jobs)):
            # 前兩則為廣告職位略過
            if i <= 2:
                continue
            companyName = jobs[i]['data-cust-name']
            companyInfo = jobs[i].find('a')
            jd = jobs[i].find('p', {'class': 'job-list-item__info'}).text
            jobTitle = companyInfo.text
            companyUrl = 'https:' + companyInfo['href']
            if '前端' in jobTitle or 'PHP' in jobTitle or 'php' in jobTitle or '實習生' in jobTitle or 'Intern' in jobTitle:
                pass
            else:
                with open('job_data.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [companyName, jobTitle, jd, companyUrl, current_datetime_str])

        time.sleep(2)

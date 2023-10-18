import asyncio
import aiohttp
import csv
import time
from bs4 import BeautifulSoup
import datetime

'''
compare with asyncio 
ref:https://myapollo.com.tw/blog/begin-to-asyncio/
>> python crawler.104.py  0.89s user 0.27s system 6% cpu 17.813 total
crawler.104.py：
執行時間：0.89秒（user），0.27秒（system），總共17.813秒。
這個版本使用的是同步（synchronous）的方式處理網路請求，即一次只處理一個請求，等待請求完成後再處理下一個。
這種方式在爬取多個網頁時，需要按照順序依次發送請求，並等待每個請求的響應。這樣的方式效率相對較低，因為大部分的時間都在等待網絡響應。

>> python crawler.async.104.py  0.66s user 0.05s system 58% cpu 1.203 total
crawler.async.104.py：
執行時間：0.66秒（user），0.05秒（system），總共1.203秒。
這個版本使用了異步（asynchronous）的方式處理網路請求，使用了asyncio和aiohttp庫，允許多個網絡請求並行處理，而不需要等待每個請求完成。
異步程式碼可以更有效地利用CPU，因為它允許同時處理多個請求，而不是按照順序進行。
CPU 使用率相對較高，因為在等待 I/O 完成的同時，CPU 可以執行其他任務。

'''


async def fetch_url(session, url, page):
    requestURL = f'{url}&page={page}'
    async with session.get(requestURL) as response:
        html = await response.text()
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        print(f'===== 第{page}頁 =====')
        print(current_datetime_str)
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find_all('article', {'class': 'job-list-item'})

        if not jobs:
            print('=== 頁面無資料 ===')
            return

        for i in range(len(jobs)):
            if i <= 2:
                continue
            companyName = jobs[i]['data-cust-name']
            companyInfo = jobs[i].find('a')
            jd = jobs[i].find('p', {'class': 'job-list-item__info'}).text
            jobTitle = companyInfo.text
            companyUrl = 'https:' + companyInfo['href']
            if '前端' in jobTitle or 'PHP' in jobTitle or 'php' in jobTitle or '實習生' in jobTitle or 'Intern' in jobTitle or '設計師' in jobTitle:
                pass
            else:
                with open('job_data.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [companyName, jobTitle, jd, companyUrl, current_datetime_str])


async def main():
    urls = [
        'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&kwop=7&keyword=Node.js%20JavaScript&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=12&asc=0&page=2&jobexp=1%2C3&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
        'https://www.104.com.tw/jobs/search/?ro=0&isnew=3&keyword=python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=1&asc=0&page=1&jobexp=1%2C3&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
        'https://www.104.com.tw/jobs/search/?ro=0&isnew=0&kwop=7&keyword=%E5%BE%8C%E7%AB%AF&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
        'https://www.104.com.tw/jobs/search/?ro=0&isnew=0&keyword=%E8%BB%9F%E9%AB%94%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001002000%2C6001001000&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob',
    ]
    pages = 3
    try:
        async with aiohttp.ClientSession() as session:
            start = time.time()
            tasks = []
            for url in urls:
                for p in range(pages):
                    task = fetch_url(session, url, p)
                    tasks.append(task)

            await asyncio.gather(*tasks)
    except Exception as e:
        print(f'爬蟲錯誤: {str(e)}')

    print(f'time:{time.time()- start}')
    # time:0.9519691467285156s

if __name__ == '__main__':
    asyncio.run(main())

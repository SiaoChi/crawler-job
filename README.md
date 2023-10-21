# crawler-job

## Introduction

This is a crawler for helping finding a software job inclued different keyword. you can use your original setting in the 104 url.


## run crawler
```
$ source myenv/bin/activate
$ python crawler.104.py
```

## crontab setting

####  1. open crontab in your terminal

```
$ crontab -e
```

####  2. use vim to insert auto setting
cd to the repo of your project and executive the relative file  as following. for the case of it, it will auto run the crawler.104.py at 11:00 am everyday.
and you can add ` >> /Users/KellyGuo/crawler/cron.log 2>&1` to add crontab log.

```
* 11 * * * cd /Users/KellyGuo/crawler/ && /Users/KellyGuo/opt/anaconda3/bin/python crawler.104.py >> /Users/KellyGuo/crawler/cron.log 2>&1
```


## Author 

- [@KellyGuo](https://www.github.com/siaochi)


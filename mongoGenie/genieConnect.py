import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbgenie

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

charts = soup.select('.list-wrap > tbody > .list')

rank = 1
for chart in charts:
    info = chart.select_one('.info')
    if info is not None:
        title = info.select_one('.title').text.strip()
        artist = info.select_one('.artist').text

        doc = {
            'rank': rank,
            'title': title,
            'artist': artist
        }
        db.dbgenie.insert_one(doc)
        rank += 1


###11번가 웹크롤링
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

req = requests.get('http://search.11st.co.kr/Search.tmall?kwd=%25EB%25AF%25B8%25EC%2584%25B8%25EB%25A8%25BC%25EC%25A7%2580%25EB%25A7%2588%25EC%258A%25A4%25ED%2581%25AC#pageNum%%3')
html = req.text
soup = BeautifulSoup(html, 'html.parser')


## 포커스클릭 + 파워상품 - 첫번째 페이지구조
title = []
s_price = []
title_f = []

for t in soup.select('div.list_info > p > a'):
    title.append(t.text)

for sp in soup.select('div > div.list_price > div.price_box > span.price_detail > strong'):
    s_price.append(sp.text)

for i in title:
    text = re.sub('\n', '', i)
    title_f.append(text)



df = pd.DataFrame(title_f, s_price)
print(df)


## 플러스상품 - 2번째 페이지부터 플러스상품만 뜸
title2 = []
s_price2 = []

for t2 in soup.select('div > div.list_info > p > a'):
    title2.append(t2.text)

for sp2 in soup.select('div > div.list_price > div.price_box > span > strong'):
    s_price2.append(sp2.text)

title_f2 = []

for i in title2:
    text2 = re.sub('\n', '', i)
    title_f2.append(text2)

df2 = pd.DataFrame(title_f2, s_price2)
print(df2)

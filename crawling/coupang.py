import requests
import re
import json
import math
import pandas as pd
import datetime
import requests
import urllib.request
import urllib.error
import urllib.parse
import requests
import itertools
from bs4 import BeautifulSoup
import time


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'
}

# list for dataframe
product_index_list = []
product_name_list = []
base_price_list = []
price_value_list = []

# url form
# https://www.coupang.com/np/search?q=미세먼지마스크&channel=auto&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=2&rocketAll=false&searchIndexingToken=
def get_search_url(search_word, page):
    search_url = "https://www.coupang.com/np/search?component=&q=" + str(search_word) + "&channel=auto&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=" + str(page) + "&rocketAll=false&searchIndexingToken="
    return search_url



def get_product_html(search_url):
    time.sleep(3)
    get_content_code = requests.get(search_url, headers=headers)
    get_content_soup = BeautifulSoup(get_content_code.content, 'lxml')
    # print(get_content_soup)

    product_data = get_content_soup.select("#productList")
    product_text = ''.join(str(x) for x in product_data)
    product_soup = BeautifulSoup(product_text, 'lxml')
    # print(product_soup)

    return product_soup



def get_product_index(product_soup):
    product_list = product_soup.find_all('ul')[0].get('data-products')
    product_index = json.loads(product_list)['indexes']
    # print(product_index)

    return product_index



def get_each_product_data(product_soup, index_num):
    each_product_soup = product_soup.find_all('li')[index_num].find_all('a')[0].find_all('div')[0]

    product_name = each_product_soup.find_all('div', {'class' : 'name'})[0].text
    price_value = each_product_soup.find_all('strong', {'class' : 'price-value'})[0].text

    try:
        base_price = each_product_soup.find_all('del', {'class' : 'base-price'})[0].text
    except IndexError:
        base_price = ''

    product_name_list.append(product_name)
    base_price_list.append(base_price)
    price_value_list.append(price_value)







if __name__ == '__main__':
    search_start_count = range(5)
    search_url_list = []

    # get each page url
    for page_num in search_start_count:
        search_url = get_search_url('미세먼지+마스크+100매', page_num)
        search_url_list.append(search_url)

    # get and enter data into the list
    for search_url in search_url_list:
        product_soup = get_product_html(search_url)
        print(serch_url)
        product_index = get_product_index(product_soup)
        product_index_list.append(product_index)

        for index_num in range(len(product_soup.find_all('li'))):
            get_each_product_data(product_soup, index_num)


    # create dataframe for final data storage
    data = {'product_index':product_index_list, 'product_name':product_name_list, 'base_price':base_price_list, 'price_value':price_value_list}
    product_df = pd.DataFrame(data)

    # Check data frames
    print(product_df.head(20))

    # Export csv file
    product_df.to_csv("coupang_mask_190411.csv", mode='w')

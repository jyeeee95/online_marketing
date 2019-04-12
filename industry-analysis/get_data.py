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


permymd_list = []
seq_list = []
bupnm_list = []
repsntnm_list = []
sidonm_list = []
dmnnm_list = []
mngstatecode_list = []

ServiceKey = 'YXPm4mAU%2BE3X6uM0ejs9kD85q4hAx5gz9v2UbgzCJsTgwDvRTs0yVAlvw%2BN0wpkA3nnltgEuCbAeMOpleQG%2F3g%3D%3D'


def get_total_page_num(url):
    get_content_code = requests.get(url)
    get_content_soup = BeautifulSoup(get_content_code.content, 'lxml')
    totalcount = get_content_soup.find_all('totalcount')[0].text
    print(totalcount)

    lastpage = round(int(totalcount)/10,0)

    return lastpage



def get_url_list(state_code, last_page_num):
    url_list = []

    for page_num in range(int(last_page_num)):
        url_list.append(url)

    return url_list



def get_content_soup(url):
    get_content_code = requests.get(url)
    get_content_soup = BeautifulSoup(get_content_code.content, 'lxml')

    product_data = get_content_soup.select("items")
    product_text = ''.join(str(x) for x in product_data)
    product_soup = BeautifulSoup(product_text, 'lxml')

    return product_soup



def get_data_list(product_soup):
    for item_num in range(10):
        item = product_soup.find_all('item')[item_num]

        try:
            permymd = item.find_all('permymd')[0].text
        except IndexError:
            permymd = ''

        try:
            seq = item.find_all('seq')[0].text
        except IndexError:
            seq = ''

        try:
            bupnm = item.find_all('bupnm')[0].text
        except IndexError:
            bupnm = ''

        try:
            sidonm = item.find_all('sidonm')[0].text
        except IndexError:
            sidonm = ''

        try:
            repsntnm = item.find_all('repsntnm')[0].text
        except IndexError:
            repsntnm = ''

        try:
            dmnnm = item.find_all('dmnnm')[0].text
        except IndexError:
            dmnnm = ''

        try:
            mngstatecode = item.find_all('mngstatecode')[0].text
        except IndexError:
            mngstatecode = ''

        permymd_list.append(permymd)
        seq_list.append(seq)
        bupnm_list.append(bupnm)
        repsntnm_list.append(repsntnm)
        sidonm_list.append(sidonm)
        dmnnm_list.append(dmnnm)
        mngstatecode_list.append(mngstatecode)



if __name__ == '__main__':
    # init setting
    state_code = '01'
    start_date = '20180101'
    end_date = '20181231'
    page_num = '1' # sample number

    # url form
    url = 'http://apis.data.go.kr/1130000/MllInfoService/getMllInfo?mngStateCode='+state_code+'&pageNo='+page_num+'&fromPermYmd='+start_date+'&toPermYmd='+end_date+'&ServiceKey='+ServiceKey


    last_page_num = get_total_page_num(url)
    url_list = get_url_list(state_code, last_page_num)

    for url in url_list:
        product_soup = get_content_soup(url)
        get_data_list(product_soup)




    # create dataframe for final data storage
    data = {'permymd' : permymd_list, 'seq' : seq_list, 'bupnm' : bupnm_list, 'repsntnm' : repsntnm_list, 'sidonm' : sidonm_list, 'dmnnm' : dmnnm_list, 'mngstatecode' : mngstatecode_list}
    final_df = pd.DataFrame(data)

    # Check data frames
    print(final_df.head(20))

    # Export csv file
    final_df.to_csv("01_180101to181231.csv", mode='w')

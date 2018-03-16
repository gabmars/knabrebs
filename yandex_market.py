import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data=pd.DataFrame()
for idx in range(300000):
    print(idx)
    try:
        url='https://market.yandex.ru/shop/'+str(idx)
        
        resp=requests.get(url)
        soup=BeautifulSoup(resp.text,'lxml')
        
        jur_info=json.loads(soup.find('div',{'class':'n-shop-address i-bem'})['data-bem'])['n-shop-address']
        data=data.set_value(idx,'Address',jur_info['juridicalAddress'])
        data=data.set_value(idx,'Name',jur_info['name'])
        data=data.set_value(idx,'OGRN',jur_info['regNum'])
        data=data.set_value(idx,'Phone',json.loads(soup.find('span',{'class':'n-phone shop-history i-bem'})['data-bem'])['n-phone']['phone']['clean'])
        data=data.set_value(idx,'Web',soup.find('a',{'class':'link n-shop-hub-info__shop-url'}).text)
    except:
        pass



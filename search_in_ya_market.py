import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

top100=pd.read_excel('top100.xlsx',header=None,names=['Web'])
data=pd.DataFrame()
proxy={'http':'195.190.124.202:8080','https':'195.190.124.202:8080'}
for i,w in enumerate(top100.values.ravel()):
#    print(i)
#    try:
    url='https://yandex.ru/yandsearch?text={}%20%D0%BE%D1%82%D0%B7%D1%8B%D0%B2%D1%8B&lr=54'.format(w)
    resp=requests.get(url,proxies=proxy)
    resp.encoding='utf8'
    soup=BeautifulSoup(resp.text,'lxml')
    for l in soup.find_all('li',{'class':'serp-item'}):
        print(l.find('a')['href'])
        if 'yandex' in l.find('a')['href']:
            idx=l.find('a')['href'].split('/')[4]
            break
    url='https://market.yandex.ru/shop/'+str(idx)
    
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,'lxml')
    try:
        jur_info=json.loads(soup.find('div',{'class':'n-shop-address i-bem'})['data-bem'])['n-shop-address']
        data=data.set_value(i,'Address',jur_info['juridicalAddress'])
        data=data.set_value(i,'Name',jur_info['name'])
        data=data.set_value(i,'Jur',jur_info['regNum'])
    except:
        pass
    data=data.set_value(i,'Phone',json.loads(soup.find('span',{'class':'n-phone shop-history i-bem'})['data-bem'])['n-phone']['phone']['clean'])
    data=data.set_value(i,'Web',soup.find('a',{'class':'link n-shop-hub-info__shop-url'}).text)
    data=data.set_value(i,'YandexId',idx)
    break

#    except Exception as e:
#        print(str(e))
#        pass


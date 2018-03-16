import pandas as pd
import requests
from bs4 import BeautifulSoup

df=pd.read_excel('non_kbk.xlsx')

for i in df.index:
    print(i)
    try:
        url='https://its.1c.ru/kbk/find/?code={}'.format(df['kbk'][i])
        resp=requests.get(url)
        soup=BeautifulSoup(resp.text,'lxml')
    except Exception as e:
        print(str(e))
        df=df.set_value(i,'descr','Error')
    else:
        try:
            df=df.set_value(i,'descr',soup.find_all('div',{'class':'panel-body'})[1].text.strip())
        except:
            df=df.set_value(i,'descr',soup.find('div',{'class':'alert alert__error'}).text.strip())

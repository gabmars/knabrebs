import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

urls=[]
urls.append('https://www.glavbukh.ru/doc/5182-spravochnik-kodov-byudjetnoy-klassifikatsii-na-2012-god')

urls.append('https://www.glavbukh.ru/doc/5623')

urls.append('https://www.glavbukh.ru/doc/5624')

urls.append('https://www.glavbukh.ru/doc/5625-spravochnik-kodov-byudjetnoy-klassifikatsii-kbk-na-2015-god')

urls.append('https://www.glavbukh.ru/doc/5636-kbk-2016-kody-byudjetnoy-klassifikatsii-kbk-na-2016-god')

for i,url in enumerate(urls):
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,'lxml')
    
    spr=pd.DataFrame()
    
    for kbk in soup.find('tbody').find_all('tr')[1:]:
        try:
            kbk['align']
            group=kbk.text.strip()
        except:
            try:
                row=[]
                row.append(group)
                row.append(kbk.find_all('td')[0].text)
                for k in kbk.find_all('td')[1:]:
                    row.append(k.text.replace(' ','').replace('–',''))
                spr=spr.append([row],ignore_index=True)
            except:
                pass
    spr=spr.fillna('')
    spr.columns=['group','descr','payment','penalty','fine']
    spr.to_excel('kbk{}.xlsx'.format(str(12+i)),index=None)
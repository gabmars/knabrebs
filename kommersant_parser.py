import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re

data=pd.DataFrame()

begin=datetime.datetime.strptime('2007-07-02','%Y-%m-%d')

url='https://www.kommersant.ru/archive/rubric/2/{}'

main_url='https://www.kommersant.ru'

while begin.date()<datetime.datetime.today().date():
    try:
        resp=requests.get(url.format(begin.strftime('%Y-%m-%d')),timeout=3)
        soup=BeautifulSoup(resp.text, 'lxml')
        for i, l in enumerate([l['href'] for l in soup.find('section',{'class':'b-other_docs'}).find_all('a') if 'rubric' not in l['href']]):
            print('{} {}'.format(str(begin.date()), i))
            try:
                res=requests.get(main_url+l,timeout=3)
                sup=BeautifulSoup(res.text, 'lxml')
                data=data.append([[main_url+l, ' '.join(re.split('\s',sup.find('div',{'id':'divLetterBranding'}).text))]],ignore_index=True)
            except:
                pass
    except:
        pass
    finally:
        begin+=datetime.timedelta(1)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading
import numpy as np

class Async(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self) 
        self.n=n
    def run(self):
        try:
            head={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'reestr.nostroy.ru',
            'Referer':'http://reestr.nostroy.ru/reestr',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'X-Compress':'null'}
            url='http://reestr.nostroy.ru/reestr?sort=m.id&direction=ASC&page={}'.format(self.n)
##            proxy={'http':'91.185.32.46:53281'}   
##            resp=requests.get(url,headers=head,proxies=proxy)
            resp=requests.get(url,headers=head)
            soup=BeautifulSoup(resp.text,'lxml')
            tbody=soup.find('table',{'class':'items table table-selectable-row table-striped'}).find('tbody')
            table=tbody.find_all('tr',{'class':'sro-link'})
            data=pd.DataFrame() 
            for tb in table:
                row=[]
                for td in tb.find_all('td'):
                    row.append(td.text.strip())
                data=data.append([row],ignore_index=True)
            data.to_excel('reestr\\Реестр членов СРО({}).xlsx'.format(self.n),index=None)
            print(self.n)
        except Exception as e:
            print(e)
        finally:
            try:
                del data
            except:
                pass

head={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'reestr.nostroy.ru',
        'Referer':'http://reestr.nostroy.ru/reestr',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Compress':'null'}
url='http://reestr.nostroy.ru/reestr'
resp=requests.get(url,headers=head)
soup=BeautifulSoup(resp.text,'lxml')
npage_ref=soup.find('ul',{'class':'pagination'}).find_all('li')[-1].find('a')['href']
npages=int(npage_ref[npage_ref.find('page=')+5:])
batch=10
lp=list(range(npages))
for b in range(int(np.ceil(npages/batch))):
    if b >= 100:
        th=[]
        for i,p in enumerate(lp[b*batch:(b+1)*batch]):
            th.append(Async(p+1))
            th[i].start()
        for t in th:
            t.join()

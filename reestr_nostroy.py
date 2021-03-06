import pandas as pd
import requests
from bs4 import BeautifulSoup

url='http://reestr.nostroy.ru/?sort=u.registrationnumber&direction=ASC&page=1'

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

data=pd.DataFrame()
url='http://reestr.nostroy.ru/'
proxy={'http':'185.64.208.230:53281'}
resp=requests.get(url,headers=head,proxies=proxy)
soup=BeautifulSoup(resp.text,'lxml')
npage_ref=soup.find('ul',{'class':'pagination'}).find_all('li')[-1].find('a')['href']
npages=int(npage_ref[npage_ref.find('page=')+5:])
for p in range(npages):
    print(p+1)
    url='http://reestr.nostroy.ru/?sort=u.registrationnumber&direction=ASC&page={}'.format(p+1)
    resp=requests.get(url,headers=head)
    soup=BeautifulSoup(resp.text,'lxml')
    tbody=soup.find('table',{'class':'items table table-striped table-selectable-row '}).find('tbody')
    table=tbody.find_all('tr',{'class':'sro-link'})
    for tb in table:
        row=[]
        for td in tb.find_all('td'):
            row.append(td.text.strip())
        data=data.append([row],ignore_index=True)

cols=[]
for c in soup.find('table',{'class':'items table table-striped table-selectable-row '}).find('thead').find('tr').find_all('th'):
    cols.append(c.text.strip())
data.columns=[cols]
##data.to_csv('Реестр СРО.csv',index=None,sep=';')

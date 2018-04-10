import requests
from bs4 import BeautifulSoup
import pandas as pd
from winreg import OpenKey,HKEY_CURRENT_USER,CloseKey,KEY_WRITE,SetValueEx,REG_DWORD

url='http://nko.economy.gov.ru/organization?tsMasterTable-page={}'

data=pd.DataFrame()
for n in range(11288):
    print(n)
    res=requests.get(url.format(n))
    soup=BeautifulSoup(res.text,'lxml')
    for tr in soup.find('table',{'id':'tsDataTable'}).find('tbody').find_all('tr'):
        data=data.append([[td.text for td in tr.find_all('td')]],ignore_index=True)

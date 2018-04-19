import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from winreg import OpenKey,HKEY_CURRENT_USER ,CloseKey,KEY_WRITE,SetValueEx,REG_DWORD

keyval=r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
Registrykey= OpenKey(HKEY_CURRENT_USER, keyval, 0,KEY_WRITE)
SetValueEx(Registrykey,"ProxyEnable",0,REG_DWORD,0)
CloseKey(Registrykey)

df=pd.DataFrame()
for i in range(2):
    url='https://news.sportbox.ru/business?page_offset={}000&page_size=1000&plain_content=1'.format(i+1)
    main_url='https://news.sportbox.ru'
    
    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,'lxml')
    
    links=[l.find('a')['href'] for l in soup.find('ul',{'class':'list'}).find_all('li')]
    text={}
    for n,l in enumerate(links):
        print(n)
        resp=requests.get(main_url+l )
        soup=BeautifulSoup(resp.text,'lxml')
        df=df.append([[l,' '.join(re.split('\s',soup.find('div',{'class':'node-content__body'}).text)).strip()]],ignore_index=True)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

data=pd.DataFrame()

webs=pd.read_excel('top100.xlsx',header=None,names=['web'])
#%%
for i,web in enumerate(webs.sample(frac=True).values.ravel()):
    print(i)
    session=requests.Session()
#    session.proxies={'http':'173.212.203.209:3128','https':'85.198.110.182:3128'}
    data=data.set_value(i,'web',web)
    try:
        if 'http' not in web:
            resp=session.get('http://'+web)
        else:
            resp=session.get(web)
    except:
        data=data.set_value(i,'<title>','')
        data=data.set_value(i,'<keywords>','')
    else:
        soup=BeautifulSoup(resp.text, 'lxml')
        try:
            data=data.set_value(i,'<title>',soup.find('title').text)
        except:
            data=data.set_value(i,'<title>','')
        try:
            data=data.set_value(i,'<keywords>',soup.find('keywords').text)
        except:
            data=data.set_value(i,'<keywords>','')
    dgis='https://www.google.ru/search?newwindow=1&ei=wn6nWq73J4uxsQGCmaSIAg&q=2gis+%26+{0}&oq=2gis+%26+{0}&gs_l=psy-ab.3...706668.708130.0.708636.6.6.0.0.0.0.177.527.0j3.3.0....0...1c.1.64.psy-ab..3.0.0....0.-PTS2M_KmXs'.format(web)
    try:
        resp=session.get(dgis)
        print(resp)
        print(resp.reason)
        soup=BeautifulSoup(resp.text, 'lxml')
        resp=session.get(soup.find('cite').text)
        print(resp)
        print(resp.reason)
        soup=BeautifulSoup(resp.text, 'lxml')
    except:
        pass
    else:
        try:
            data=data.set_value(i,'Phones',';'.join([ph['href'].replace('tel:+','') for ph in soup.find('div',{'class':'contact'}).find_all('a',{'class':'contact__phonesItemLink'})]))#phones
        except:
            data=data.set_value(i,'Phones','')        
        try:
            for sl in soup.find('div',{'class':'contact'}).find('div',{'class':'contact__socials'}).find_all('a'):#social_links
                try:
                    data=data.set_value(i,sl.text,sl['href'])
                except:
                    pass
        except:
            pass
        try:
            data=data.set_value(i,'Payments',';'.join([l.text for l in soup.find('ul',{'class':'card__payment'}).find_all('li')]))#payment
        except:
            data=data.set_value(i,'Payments','')    
        try:
            data=data.set_value(i,'Address',soup.find('span',{'class':'card__addressPart'}).text)#address
        except:
            data=data.set_value(i,'Address','')    
        try:
            name=soup.find('h1',{'class':'cardHeader__headerNameText'}).text#name
        except:
            data=data.set_value(i,'Name','')
            data=data.set_value(i,'INN','')
            data=data.set_value(i,'OGRN','')
        else:            
            data=data.set_value(i,'Name',name)    
            try:
                name+='.'
                add='http://uninformer.azurewebsites.net/api/Values/{}'.format(name[:name.find('.')])
                resp=session.get(add)
                soup=BeautifulSoup(resp.text, 'lxml')
                if 'The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.' in soup.text or 'An error has occurred.' in soup.text:
                    raise Exception()
                else:
                    info=json.loads(soup.find('p').text)
                    data=data.set_value(i,'INN',info['inn'])
                    data=data.set_value(i,'OGRN',info['ogrn'])
            except:
                data=data.set_value(i,'INN','')
                data=data.set_value(i,'OGRN','')
    break

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

webs = pd.read_excel('top300.xlsx',names=['Web'])

def check_www(url, text):
    if 'www' in text:
        return url
    else:
        return str(url) + str(text)
#%%
d = {}
words=['Контакты', 'О нас', 'Контактная информация','Реквизиты', 'Юридическая информация', 'Публичная оферта', 'Условия оферты','Контакты и реквизиты','Оплата','Доставка и оплата','Оплата и доставка']
for n,i in enumerate(webs['Web']):
    print(n)
    try:        
        url = 'http://' + str(i)
        r = requests.get(url)
        r.encoding='utf8'
        soup = BeautifulSoup(r.text, 'lxml')
        links = {re.sub("^\s+|\n|\r|\s+$", '', str(x.text)):x['href'] for x in soup.find_all('a', href=True)}              
        try:
            s = {}
            for w in words:
                if w in links.keys():
                    s[w]=links[w]
            d[i] = s
        except Exception as e:
            print('url {} No such found. Error {}'.format(i, e))
    except Exception as e:
        print('url {} not found. Error {}'.format(i,e))
#%%
d={k:v for k,v in d.items() if len(v)>0}
m = []
texts=[]
r=re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
data=pd.DataFrame()
check=[]
all_links={}
social_networks={'VK':'vk.com','OK':'ok.ru','Facebook':'facebook.com','Twitter':'twitter.com','Instagram':'instagram.com','YouTube':'youtube.com'}
for i,n in enumerate(webs.index):
    print(i)
    title=''
    meta_descr=''
    meta_kw=''
    try:
        resp=requests.get('http://'+webs['Web'][n])
        resp.encoding='utf8'
        soup=BeautifulSoup(resp.text,'lxml')
        try:
            title=soup.find('title').text
        except:
            pass
        try:
            meta_descr=soup.find('meta',{'name':'description'})['content']
        except:
            pass
        try:
            meta_kw=soup.find('meta',{'name':'keywords'})['content']
        except:
            pass
    except:
        pass
    crws=''
    ptws=''
    try:
        resp=requests.get('https://www.nic.ru/whois/?searchWord={}'.format(webs['Webs'][n]),timeout=3)
    except:
        pass
    else:
        try:
            soup=BeautifulSoup(resp.text,'lxml')
            whois=soup.find('div',{'class':'column-b'}).text
            try:
                crws=whois[whois.index('created:'):]
                crws=crws[8:crws.index('T')].strip()
            except:
                pass
            try:
                ptws=whois[whois.index('paid-till:'):]
                ptws=ptws[10:ptws.index('T')].strip()
            except:
                pass
        except:
            pass  
    if webs['Web'][n] in d.keys():
        try:
            for lnk in d[webs['Web'][n]].items():
                skip=False
                print(lnk)
                row=[]
                row.append(webs['Web'][n])
                row.append(title)
                row.append(meta_descr)
                row.append(meta_kw)
                row.append(lnk[0])
                try:
                    m.append(lnk[1])
                    if webs['Web'][n].replace('www.','').lower() not in m[-1].lower():
                        l='http://'+(webs['Web'][n]+'/'+m[-1]).replace('//','/')
                    else:
                        tm=m[-1]
                        if 'http' not in tm:
                            l='http://'+tm
                            l=l.replace('//','/')
                        else:
                            l=tm
                    row.append(l)
                    resp=requests.get(l) 
                    soup=BeautifulSoup(resp.text,'lxml')
                    links = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]
                    snetworks={'VK':'','OK':'','Facebook':'','Twitter':'','Instagram':'','YouTube':''}
                    for slnk in links:
                        for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                            if social_networks[sn] in slnk:
                                snetworks[sn]=slnk
                    for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                        row.append(snetworks[sn])
                    try:
                        texts.append(re.sub('\s',' ',soup.text).strip())
                    except:
                        pass
                    try:
                        row.append(';'.join(r.findall(texts[-1].replace('-',''))))
                    except:
                        row.append('')
                    try:
                        s=texts[-1].split('ИНН')[1].replace('-','').replace(')','').replace(':','').replace(',','').strip().split(' ')[0].replace('\\','/')
                        if s=='/КПП':
                            s=texts[-1].split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0].replace('\\','/').split('/')[0]
                            skip=True
                            row.append(s)
                            try:
                                row.append(texts[-1].split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0].replace('\\','/').split('/')[1])
                            except:
                                row.append('')
                        elif '/' in s:
                            skip=True
                            row.append(s.split('/')[0])
                            row.append(s.split('/')[1])
                        else:
                            row.append(s)
                    except:
                        row.append('')
                        if skip:
                            row.append('')
                    try:
                        if not skip:
                            row.append(texts[-1].split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0])
                    except:
                        row.append('')
                    try:
                        s=texts[-1].split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split(' ')[0]
                        if '/' in s:
                            s=texts[-1].split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split('/')[1].split(' ')[1]
                        row.append(s)                    
                    except:
                        row.append('')
                    try:
                        s=texts[-1].split('БИК')[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                        if len(s) < 9:
                            ss=texts[-1].split('БИК')[-1].replace('-','').replace(':','').strip().split(' ')
                            for i in range(1,10):
                                s=''.join(ss[:i])
                                if len(s) >= 9:
                                    break
                        row.append(s)
                    except:
                        row.append('')
                    row.append('')
                    for cs in ['Корреспондентский счет','Корреспонденский счет','Корр. счет','Кор. счет','Корр.счет','Кор.счет','кор/счет','К/счет','Кор/сч','Корр/С','Кор/с','К/сч','К/С']:
                        try:
                            s=texts[-1].lower().replace('\\','/').split(cs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                            s=re.sub('\D','',s)
                            if s != '':
                                if len(s) < 20:
                                    ss=texts[-1].lower().replace('\\','/').split(cs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')
                                    for i in range(1,20):
                                        s=''.join(ss[:i])
                                        if len(s) >= 20:
                                            break
                                s=re.sub('\D','',s)
                                if (s != row[-1]) & (s != '') & (len(s)>=20):
                                    row[-1]=s
                                    break
                        except:
                            pass
                    row.append('')
                    for rs in ['Расчетный счет','Рассч/С','Р/Счет','Р/сч','Р/С']:
                        try:
                            s=texts[-1].lower().replace('\\','/').split(rs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                            s=re.sub('\D','',s)
                            if (s != row[-1]) & (s != ''):
                                if len(s) < 20:
                                    ss=texts[-1].lower().replace('\\','/').split(rs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')
                                    for i in range(1,20):
                                        s=''.join(ss[:i])
                                        if len(s) >= 20:
                                            break
                                s=re.sub('\D','',s)
                                if (s != row[-1]) & (s != '') & (len(s)>=20):
                                    row[-1]=s
                                    break
                        except:
                            pass
                    try:
                        row.append(';'.join(re.findall(r'[\w\.-]+@[\w\.-]+', texts[-1])))
                    except:
                        row.append('')
                    row.append(crws)
                    row.append(ptws)
                    row.append('')
                    for pmnt in ['безнал','банковск','пластиков','visa','mastercard','americanexpress','master card','american express','кредитн']:
                        try:
                            texts[-1].index(pmnt)
                            row[-1]='1'
                            break
                        except:
                            pass
                    data=data.append([row],ignore_index=True)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))
    else:
        row=[]
        row.append(webs['Web'][n])
        row.append(title)
        row.append(meta_descr)
        row.append(meta_kw)
        row.extend(['']*16)
        row.append(crws)
        row.append(ptws)
        row.append('')
        data=data.append([row],ignore_index=True)
#%%
data.columns=['Web','<Title>','<Description>','<Keywords>','LinkType','Link','VK','OK','Facebook','Twitter','Instagram','YouTube','Phones','INN','KPP','OGRN','BIK','CS','RS','Email','DomainRegDate','DomainExpiryDate','Payment']
data=data[['Web','<Title>','<Description>','<Keywords>','LinkType','Link','INN','KPP','OGRN','BIK','CS','RS','Phones','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','DomainRegDate','DomainExpiryDate','Payment']]
data=data.fillna('')
data['INN']=data['INN'].apply(lambda x: re.sub('\D','',x))
data['KPP']=data['KPP'].apply(lambda x: re.sub('\D','',x))
data['OGRN']=data['OGRN'].apply(lambda x: re.sub('\D','',x))
data['BIK']=data['BIK'].apply(lambda x: re.sub('\D','',x))
data['CS']=data['CS'].apply(lambda x: re.sub('\D','',x))
data['RS']=data['RS'].apply(lambda x: re.sub('\D','',x))

for col in ['INN','KPP','OGRN','BIK','CS','RS']:
    for i in data.loc[(data[col].apply(len)<8) & (data[col]!='')].index:
        data=data.set_value(i,col,'')
res=pd.DataFrame()
for n,i in enumerate(data['Web'].drop_duplicates().values.ravel()):
    sdf=data.loc[data['Web']==i].copy()
    lll={}
    for lt,ll in zip(sdf['LinkType'].values.ravel(),sdf['Link'].values.ravel()):
        lll[lt]=ll
    for col in ['Web','<Title>','<Description>','<Keywords>']:
        res=res.set_value(n,col,sdf[col].values.ravel()[0])
    res=res.set_value(n,'Links',str(lll))
    for col in ['INN','KPP','OGRN','BIK','CS','RS','Phones','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','DomainRegDate','DomainExpiryDate','Payment']:
        res=res.set_value(n,col,sdf.loc[sdf[col].apply(len)==sdf[col].apply(len).max()][col].values.ravel()[0])        
res.to_excel('ecom_result.xlsx',index=None)

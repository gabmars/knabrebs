import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import multiprocessing as mp
import warnings
import os
import sys
warnings.simplefilter(action='ignore', category=FutureWarning)

ip2=[7,2,4,10,3,5,9,4,6,8]
ip1=[3,7,2,4,10,3,5,9,4,6,8]
ul=[2,4,10,3,5,9,4,6,8]

def check_inn(inn):
    if len(inn)==9 or len(inn)==11:
        inn='0'+inn
    elif len(inn)<9 or len(inn)>12:
        return False
    if len(inn)==12:
        chck_sum=0
        for i,n in enumerate(inn[:10]):
            chck_sum+=int(n)*ip2[i]
        print(chck_sum)
        if str(chck_sum%11)[-1]!=inn[10]:
            return False
        chck_sum=0
        for i,n in enumerate(inn[:11]):
            chck_sum+=int(n)*ip1[i]
        print(chck_sum)
        if str(chck_sum%11)[-1]!=inn[11]:
            return False
        return True
    if len(inn)==10:
        chck_sum=0
        for i,n in enumerate(inn[:9]):
            chck_sum+=int(n)*ul[i]
        if str(chck_sum%11)[-1]!=inn[9]:
            return False
        return True

def check_ogrn(ogrn):
    if len(ogrn)==13:
        if str(int(ogrn[:12])%11)[-1]!=ogrn[-1]:
            return False
        return True
    if len(ogrn)==15:
        if str(int(ogrn[:14])%11)[-1]!=ogrn[-1]:
            return False
        return True

start_time=datetime.datetime.now()

webs=pd.read_csv('ihead_domains_sept_2017.csv',encoding='1251',sep=';')
#%%
webs=webs.head(100)
#%%
l=webs[['домен','дата']].values.tolist()
chunk_size=20
chunks=[l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]
#%%
def scan(inpt,data):
    def check_www(url, text):
        if 'www' in text: 
            return url
        else:
            return str(url) + str(text)

    words=['Компания','О компании','Контакты', 'О нас', 'Контактная информация','Реквизиты', 'Юридическая информация', 'Публичная оферта', 'Условия оферты','Контакты и реквизиты','Оплата','Доставка и оплата','Оплата и доставка']
    social_networks={'VK':'vk.com','OK':'ok.ru','Facebook':'facebook.com','Twitter':'twitter.com','Instagram':'instagram.com','YouTube':'youtube.com'}
    for inp  in inpt:
        sweb=inp[0]
        sys.stdout=open('log\\{}.counter_log'.format(str(len(data))),'w')
        print(len(data))
        title=''
        meta_descr=''
        meta_kw=''
        whois=''
        try: 
            resp=requests.get('http://'+sweb,timeout=3)
            web=resp.url
            for sw in ['https','http',':','/','www.']:
                web=web.replace(sw,'')
            web=web.encode('utf8').decode('idna')
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
            web=sweb
            pass
        try: 
            links = {re.sub("^\s+|\n|\r|\s+$", '', str(x.text)):x['href'] for x in soup.find_all('a', href=True)}              
        except:
            links = dict()
        crws=''
        ptws=''
        try:
            resp=requests.get('https://www.nic.ru/whois/?searchWord={}'.format(web),timeout=3)
        except:
            pass
        else: 
            try:
                whois_soup=BeautifulSoup(resp.text,'lxml')
                whois=whois_soup.find('ul',{'class':'_3U-mA _23Irb'}).text
                try:
                    crws=whois[whois.index('created:'):]
                    crws=crws[8:18]
                    crws=re.sub('\D','.',crws)
                    if len(crws.split('.')[0]) == 4:
                        crws=crws.split('.')[2]+'.'+crws.split('.')[1]+'.'+crws.split('.')[0]
                except:
                    pass
                try:
                    ptws=whois[whois.index('till:'):]
                    ptws=ptws[5:15]
                    ptws=re.sub('\D','.',ptws)
                    if len(ptws.split('.')[0]) == 4:
                        ptws=ptws.split('.')[2]+'.'+ptws.split('.')[1]+'.'+ptws.split('.')[0]
                except:
                    pass
            except:
                pass
        try:
            d={w:links[w].replace('../','') for w in words if w in links and len(links[w])>0}
        except Exception as e:
            d={}
        if len(d) > 0:
            try:
                for lnk in d.items():
                    if web.replace('www.','').lower() not in lnk[1].lower():
                        l='http://'+(web+'/'+lnk[1]).replace('//','/')
                    else:
                        tm=lnk[1]
                        if 'http' not in tm:
                            l='http://'+tm
                            l=l.replace('//','/')
                        else:
                            l=tm
                    resp=requests.get(l,timeout=3) 
                    new_soup=BeautifulSoup(resp.text,'lxml')
                    for x in new_soup.find_all('a', href=True):
                        k=re.sub("^\s+|\n|\r|\s+$", '', str(x.text))
                        v=x['href']
                        if k not in list(d.keys()) and k in words and len(v)>0 and k != v:
                            d[k]=v.replace('../','')
            except:
                pass
            try:
                for lnk in d.items():
                    skip=False
                    print(lnk)
                    row=[]
                    row.append(sweb)
                    row.append(inp[1])
                    row.append(web)
                    row.append(title)
                    row.append(meta_descr)
                    row.append(meta_kw)
                    row.append(lnk[0])
                    try: 
                        if web.replace('www.','').lower() not in lnk[1].lower():
                            l='http://'+(web+'/'+lnk[1]).replace('//','/')
                        else:
                            tm=lnk[1]
                            if 'http' not in tm:
                                l='http://'+tm
                                l=l.replace('//','/')
                            else:
                                l=tm
                        row.append(l)
                        resp=requests.get(l,timeout=3) 
                        soup=BeautifulSoup(resp.text,'lxml')
                        slinks = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]
                        snetworks={'VK':'','OK':'','Facebook':'','Twitter':'','Instagram':'','YouTube':''}
                        for slnk in slinks:
                            for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                                if social_networks[sn] in slnk:
                                    snetworks[sn]=slnk
                        for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                            row.append(snetworks[sn])
                        try:
                            text=re.sub('\s',' ',soup.text).strip()
                        except:
                            text=''
                        try:
#                            r=re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
                            phones=[s for s in re.sub('\D',' ',re.sub('[^\w\s]','',text)).split(' ') if s != '' and len(s) in [7,10,11] and s[0] in ['7','8','3','4','9']]
                            row.append(';'.join(phones))
                        except:
                            row.append('')
                        try:
                            s=text.split(' ИНН')[1].replace('-','').replace(')','').replace(':','').replace(',','').strip().replace('/ КПП','/КПП').replace(' / ','/').split(' ')[0].replace('\\','/')
                            if s=='/КПП':
                                s=text.split(' КПП')[1].replace('-','').replace(')','').replace(':','').strip().replace(' / ','/').split(' ')[0].replace('\\','/').split('/')[0]
                                skip=True
                                row.append(s)
                                try:
                                    row.append(text.split(' КПП')[1].replace('-','').replace(')','').replace(':','').strip().replace(' / ','/').split(' ')[0].replace('\\','/').split('/')[1])
                                except:
                                    row.append('')
                            elif '/' in s and '/КПП'==s[:4]:
                                skip=True 
                                row.append(s.replace('/КПП','').split('/')[0])
                                try:
                                    row.append(s.replace('/КПП','').split('/')[1])
                                except:
                                    row.append('')
                            elif '/' in s and 'КПП' in s:
                                skip=True 
                                row.append(s.replace(' КПП','').split('/')[0])
                                try:
                                    row.append(s.replace(' КПП','').split('/')[1])
                                except:
                                    row.append('')
                            else: 
                                row.append(s)
                        except:
                            try:
                                s=text.split('ИНН')[1].replace('-','').replace(')','').replace(':','').replace(',','').strip().replace('/ КПП','/КПП').replace(' / ','/').split(' ')[0].replace('\\','/')
                                if s=='/КПП':
                                    s=text.split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().replace(' / ','/').split(' ')[0].replace('\\','/').split('/')[0]
                                    skip=True
                                    row.append(s)
                                    try:
                                        row.append(text.split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().replace(' / ','/').split(' ')[0].replace('\\','/').split('/')[1])
                                    except:
                                        row.append('')
                                elif '/' in s and '/КПП'==s[:4]:
                                    skip=True 
                                    row.append(s.replace('/КПП','').split('/')[0])
                                    try:
                                        row.append(s.replace('/КПП','').split('/')[1])
                                    except:
                                        row.append('')
                                elif '/' in s and 'КПП' in s:
                                    skip=True 
                                    row.append(s.replace('КПП','').split('/')[0])
                                    try:
                                        row.append(s.replace('КПП','').split('/')[1])
                                    except:
                                        row.append('')
                                else: 
                                    row.append(s)
                            except:
                                row.append('')
                                if skip:
                                    row.append('')
                        try:
                            if not skip:
                                row.append(text.split(' КПП')[1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0])
                        except:
                            try:
                                if not skip:
                                    row.append(text.split('КПП')[1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0])
                            except:
                                row.append('')
                        try:
                            s=text.split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split(' ')[0]
                            if '/' in s and 'КПП' in s:
                                s=text.split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split('/')[1].split(' ')[1]
                            row.append(s)                    
                        except:
                            row.append('')
                        try:
                            s=text.split('БИК')[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                            if len(s) < 9:
                                ss=text.split('БИК')[-1].replace('-','').replace(':','').strip().split(' ')
                                for i in range(1,10):
                                    s=''.join(ss[:i])
                                    if len(s) >= 9:
                                        break
                            row.append(s)
                        except:
                            row.append('')
                        row.append('')
                        for cs in ['Корреспондентский счет','Корреспонденский счет','Корр счет','Кор счет','Коррсчет','Корсчет','Коррсч','кор/счет','К/счет','Кор/сч','Корр/С','Кор/с','К/сч','К/С']:
                            try:
                                s=text.lower().replace('банка','').replace('банк','').replace('.','').replace('№','').replace('ё','е').replace('\\','/').split(cs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                                s=re.sub('\D','',s)
                                if s != '':
                                    if len(s) < 20:
                                        ss=text.lower().replace('ё','е').replace('\\','/').split(cs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')
                                        for i in range(1,20):
                                            s=''.join(ss[:i])
                                            if len(s) >= 20:
                                                break
                                    s=re.sub('\D','',s)
                                    if (s != row[-1]) & (s != '') & (len(s)>=18):
                                        row[-1]=s
                                        break
                            except:
                                pass
                        row.append('')
                        for rs in ['Расчетный счет','Рассч/С',' Р/Счет',' Р/сч',' Р/С','Р/Счет','Р/сч','Р/С']:
                            try:
                                s=text.lower().replace('банка','').replace('банк','').replace('.','').replace('№','').replace('ё','е').replace('\\','/').split(rs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')[0]
                                s=re.sub('\D','',s)
                                if (s != row[-1]) & (s != ''):
                                    if len(s) < 20:
                                        ss=text.lower().replace('ё','е').replace('\\','/').split(rs.lower())[-1].replace('-','').replace(')','').replace(':','').strip().split(' ')
                                        for i in range(1,20):
                                            s=''.join(ss[:i])
                                            if len(s) >= 20:
                                                break
                                    s=re.sub('\D','',s)
                                    if (s != row[-1]) & (s != '') & (len(s)>=18):
                                        row[-1]=s
                                        break
                            except:
                                pass
                        try:
                            row.append(';'.join(re.findall(r'[\w\.-]+@[\w\.-]+', text)))
                        except:
                            row.append('')
                        row.append(crws)
                        row.append(ptws)
                        row.append(whois)
                        row.append('')
                        for pmnt in ['безнал','банковск','пластиков','visa','mastercard','americanexpress','master card','american express','виза','мастеркард','мастер кард','мастер-кард','кредитн','киви','paypal','scrill','qiwi','webmoney', 'пайпал','скрилл','яндекс-деньги','яндекс.деньги','веб-мани','веб мани','яндекс деньги', 'rbk money', 'рбк мани','рапида', 'w1','liqpay','ликпей','perfectmoney','перфектмани','деньги@mail.ru', 'деньги@майл.ру']:
                            try:
                                text.index(pmnt)
                                row[-1]='1'
                                break
                            except:
                                pass
                        inns=[]
                        for n in [s for s in re.sub('\D',' ',text).split(' ') if s != '']:
                            if check_inn(n):
                                inns.append(n)
                        row.append(';'.join(inns))
                        ogrns=[]
                        for n in [s for s in re.sub('\D',' ',text).split(' ') if s != '']:
                            if check_ogrn(n):
                                ogrns.append(n)
                        row.append(';'.join(ogrns))
                        data.append(row)
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))
        else:
            row=[]
            row.append(sweb)
            row.append(inp[1])
            row.append(web)
            row.append(title)
            row.append(meta_descr)
            row.append(meta_kw)
            row.extend(['']*16)
            row.append(crws)
            row.append(ptws)
            row.append(whois)
            row.append('')
            row.append('')
            row.append('')
            data.append(row)

#%%
if __name__ == '__main__':
    for f in os.listdir('log'):
        os.remove('log\\'+f)
    mgr=mp.Manager()
    shared_list=mgr.list()
    
    prcs=[] 
    for chunk in chunks:
        p=mp.Process(target=scan, args=(chunk,shared_list,))
        prcs.append(p)
        p.start() 
    
    for p in prcs:
        p.join()
    data=pd.DataFrame(list(shared_list))

#%%
    print('Collected')
    writer = pd.ExcelWriter('ecom_temp.xlsx',options={'strings_to_urls': False})
    data.to_excel(writer,index=None)
    writer.close()
    data.columns=['In_Web','In_RegDate','Out_Web','<Title>','<Description>','<Keywords>','LinkType','Link','VK','OK','Facebook','Twitter','Instagram','YouTube','Phones','INN','KPP','OGRN','BIK','CS','RS','Email','DomainRegDate','DomainExpiryDate','WHOIS','Payment','INNS','OGRNS']
    data=data[['In_Web','Out_Web', '<Title>','<Description>','<Keywords>','LinkType','Link','INN','KPP','OGRN','BIK','CS','RS','Phones','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','In_RegDate','DomainRegDate','DomainExpiryDate','Payment','WHOIS','INNS','OGRNS']]
    data=data.fillna('')

    data['INN']=data['INN'].apply(lambda x: re.sub('\D','',x))
    data['KPP']=data['KPP'].apply(lambda x: re.sub('\D','',x))
    data['OGRN']=data['OGRN'].apply(lambda x: re.sub('\D','',x))
    data['BIK']=data['BIK'].apply(lambda x: re.sub('\D','',x))
    data['CS']=data['CS'].apply(lambda x: re.sub('\D','',x))
    data['RS']=data['RS'].apply(lambda x: re.sub('\D','',x))
    
    for i in data.loc[~data['INN'].apply(len).isin([9,10,11,12])].index:
        data=data.set_value(i,'INN','')
    for i in data.loc[~data['KPP'].apply(len).isin([8,9])].index:
        data=data.set_value(i,'KPP','')
    for i in data.loc[~data['OGRN'].apply(len).isin([12,13,14,15])].index:
        data=data.set_value(i,'OGRN','')
    for i in data.loc[~data['BIK'].apply(len).isin([8,9])].index:
        data=data.set_value(i,'BIK','')
    for i in data.loc[~data['CS'].apply(len)==20].index:
        data=data.set_value(i,'CS','')
    for i in data.loc[~data['RS'].apply(len)==20].index:
        data=data.set_value(i,'RS','')
    
    res=pd.DataFrame() 
    
    for n,i in enumerate(data['In_Web'].drop_duplicates().values.ravel()):
        sdf=data.loc[data['In_Web']==i].copy()
        lll={}
        for lt,ll in zip(sdf['LinkType'].values.ravel(),sdf['Link'].values.ravel()):
            lll[lt]=ll
        for col in ['In_Web','In_RegDate','Out_Web','<Title>','<Description>','<Keywords>','DomainRegDate','DomainExpiryDate','WHOIS']:
            res=res.set_value(n,col,sdf[col].values.ravel()[0])
        res=res.set_value(n,'Links',str(lll))
        for col in ['INN','KPP','OGRN','BIK','CS','RS','Phones','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','Payment']:
            res=res.set_value(n,col,sdf.loc[sdf[col].apply(len)==sdf[col].apply(len).max()][col].values.ravel()[0])        
        res=res.set_value(n,'INNS',';'.join(list(sdf['INNS'].values.ravel())))
        res=res.set_value(n,'OGRNS',';'.join(list(sdf['OGRNS'].values.ravel())))
    
    res['Phones']=res['Phones'].apply(lambda x: ';'.join(set(x.split(';'))))
    res['INNS']=res['INNS'].apply(lambda x: ';'.join(set([s for s in x.split(';') if s!=''])))
    res['OGRNS']=res['OGRNS'].apply(lambda x: ';'.join(set([s for s in x.split(';') if s!=''])))
    res=res[['In_Web','Out_Web', '<Title>','<Description>','<Keywords>','Links','INN','KPP','OGRN','BIK','CS','RS','Phones','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','In_RegDate','DomainRegDate','DomainExpiryDate','Payment','INNS','OGRNS','WHOIS']]

    writer = pd.ExcelWriter('ecom_result_part0.xlsx',options={'strings_to_urls': False})
    res.to_excel(writer,index=None)
    writer.close()
#%%
    print(datetime.datetime.now()-start_time)
    
    os.system('shutdown.exe /h')

import imaplib
import email

imapSession = imaplib.IMAP4_SSL('imap.gmail.com',993)
imapSession.login('ecomscanner@gmail.com','EcomS123')
imapSession.select('inbox')

typ, data = imapSession.search(None, 'ALL')
if typ=='OK':
    print(data)
    mids=data[0].split()
#    for i in mids:
#        typ, bmsg = imapSession.fetch(i, '(RFC822)' )
#        
#        if typ=='OK':    
#            for response_part in bmsg:
#                if isinstance(response_part, tuple):
#                    msg = email.message_from_string(response_part[1].decode('utf8'))
#                    
#                    for part in msg.walk():
#                        if part.get_content_maintype() =='text':
imapSession.close()     
imapSession.logout()

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import multiprocessing as mp
import warnings
import os
import json
import sys
warnings.simplefilter(action='ignore', category=FutureWarning)
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def ecom_logger(tid, message):
    print('{} {} {}'.format(str(datetime.datetime.now()), tid, message))
    with open('ecom_log', 'a') as file:
        file.write('{} {} {}'.format(str(datetime.datetime.now()), tid, message))
        file.close()

def send_mail(send_to, subject, text, files=None):
      
    msg = MIMEMultipart()
    msg['From'] = 'ecomscanner@gmail.com'
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('ecomscanner@gmail.com', 'EcomS123')
    smtp.sendmail('ecomscanner@gmail.com', send_to, msg.as_string())
    smtp.close()

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
        if str(chck_sum%11)[-1]!=inn[10]:
            return False
        chck_sum=0
        for i,n in enumerate(inn[:11]):
            chck_sum+=int(n)*ip1[i]
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

def scan(inpt,data):
    def check_www(url, text):
        if 'www' in text: 
            return url
        else:
            return str(url) + str(text)
    
    
    words=['Политика конфиденциальности','Компания','О компании','Контакты', 'О нас', 'Контактная информация','Реквизиты', 'Юридическая информация', 'Публичная оферта', 'Условия оферты','Контакты и реквизиты','Оплата','Доставка и оплата','Оплата и доставка']
    social_networks={'VK':'vk.com','OK':'ok.ru','Facebook':'facebook.com','Twitter':'twitter.com','Instagram':'instagram.com','YouTube':'youtube.com'}
    #<time_monitor>
    #general_start_time=datetime.datetime.now()
    #</time_monitor>
    for inp  in inpt:
        #<time_monitor>
    #    start_time=datetime.datetime.now()
        #</time_monitor>
        sweb=inp[0]
        sys.stdout=open('/ecomlog/{}_{}.counter_log'.format(str(len(data)), tid),'w')
        print(len(data))
        title=''
        meta_descr=''
        meta_kw=''
        main_content=''
        try: 
            resp=requests.get('http://'+sweb,timeout=3)
            resp.encoding='utf8'
            web=resp.url
            for sw in ['https','http',':','/','www.']:
                web=web.replace(sw,'')
            web=web.encode('utf8').decode('idna')
            soup=BeautifulSoup(resp.text,'lxml')
            try:
                main_content=';'.join([s for s in re.sub('\s',' ',soup.text.replace('\n',';')).split(';') if s !=''])
            except:
                pass
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
        #<time_monitor>
    #    elepsed_time['Main page']=elepsed_time.get('Main page',0)+(datetime.datetime.now()-start_time).total_seconds()
    #    
    #    start_time=datetime.datetime.now()
        #</time_monitor>
        try: 
            links = {re.sub("^\s+|\n|\r|\s+$", '', str(x.text)):x['href'] for x in soup.find_all('a', href=True)}              
        except:
            links = dict()
        #<time_monitor>
    #    elepsed_time['Links collecting']=elepsed_time.get('Links collecting',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #    start_time=datetime.datetime.now()
        #</time_monitor>
        crws=''
        ptws=''
        whois=''
        phonews=''
        emailws=''
    #    try:
    ##            resp=requests.get('https://www.nic.ru/whois/?searchWord={}'.format(web),timeout=3)
    ##            resp=requests.get('http://www.1whois.ru/?url={}'.format(web),timeout=3)
    #        resp=requests.get('https://r01.ru/domain/whois/check-domain.php?domain={}'.format(web),timeout=3)
    #    except:
    #        pass
    #    else: 
    #        try:
    #            whois_soup=BeautifulSoup(resp.text,'lxml')
    ##                whois=whois_soup.find('ul',{'class':'_3U-mA _23Irb'}).text
    ##                whois=whois_soup.find('blockquote').text
    #            whois=whois_soup.find('pre',{'class':'whois'}).text
    #            try:
    #                crws=whois[whois.index('created:'):].replace(' ','').replace('\xa0','')
    #                crws=crws[8:18]
    #                crws=re.sub('\D','.',crws)
    #                if len(crws.split('.')[0]) == 4:
    #                    crws=crws.split('.')[2]+'.'+crws.split('.')[1]+'.'+crws.split('.')[0]
    #            except:
    #                pass
    #            try:
    #                ptws=whois[whois.index('till:'):].replace(' ','').replace('\xa0','')
    #                ptws=ptws[5:15]
    #                ptws=re.sub('\D','.',ptws)
    #                if len(ptws.split('.')[0]) == 4:
    #                    ptws=ptws.split('.')[2]+'.'+ptws.split('.')[1]+'.'+ptws.split('.')[0]
    #            except:
    #                pass
    #            try:
    #                phone=whois[whois.index('phone:'):].replace('\xa0','')
    #                phone=phone[6:phone.index('e-mail:')].strip()
    #            except:
    #                try:
    #                    phone=phone[6:phone.index('e-mail:')].strip()
    #                except:
    #                    pass
    #            try:
    #                email=whois[whois.index('e-mail:'):].replace('\xa0','')
    #                email=email[7:email.index('reg-till:')].strip()
    #            except:
    #                pass
    #        except:
    #            pass
        #<time_monitor>
    #    elepsed_time['Whois processing']=elepsed_time.get('Whois processing',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #    start_time=datetime.datetime.now()
        #</time_monitor>
        try:
            d={w:links[w].replace('../','') for w in words if w in links and len(links[w])>0}
        except Exception as e:
            d={}
        #<time_monitor>
    #    elepsed_time['Links restructing']=elepsed_time.get('Links restructing',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #    start_time=datetime.datetime.now()
        #</time_monitor>
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
            #<time_monitor>
    #        elepsed_time['Links recollecting']=elepsed_time.get('Links recollecting',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #        start_time=datetime.datetime.now()
            #</time_monitor>
            try:
                for lnk in d.items():
                    skip=False
                    print(lnk)
                    row=[]
                    row.append(sweb)
                    row.append(inp[1])
                    row.append(main_content)
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
                        resp.encoding='utf8'
                        soup=BeautifulSoup(resp.text,'lxml')
                        slinks = [a['href'] for a in soup.find_all('a') if a.has_attr('href')]
                        snetworks={'VK':[],'OK':[],'Facebook':[],'Twitter':[],'Instagram':[],'YouTube':[]}
                        for slnk in slinks:
                            for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                                if social_networks[sn] in slnk:
                                    snetworks.get(sn,[]).append(slnk)
                        for sn in ['VK','OK','Facebook','Twitter','Instagram','YouTube']:
                            row.append(';'.join(snetworks[sn]))
                        #<time_monitor>
    #                    elepsed_time['Slinks']=elepsed_time.get('Slinks',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        try:
                            text=re.sub('\s',' ',soup.text).strip()
                        except:
                            text=''
                        #<time_monitor>
    #                    elepsed_time['Text']=elepsed_time.get('Text',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        try:
    #                        1.
    #                        r=re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
    #                        2.
    #                        phones=[s for s in re.sub('\D',' ',re.sub('[^\w\s]','',text)).split(' ') if s != '' and len(s) in [7,10,11] and s[0] in ['7','8','3','4','9']]
    #                        3.
    #                        ptext=soup.text
    #                        phones=[]
    #                        for l in [7,10,11]:
    #                            phones.extend(re.findall('[7,8,3,4,9]\d{%s}'%(l-1),re.sub('[^\d ]','',ptext)))
    #                        4.
                            phones={}
                            ptext=soup.get_text('\n')
                            phones_subs=set(re.findall(r'\s*(.+(?:(?=\d)).+)\s*',ptext))
                            for pss in phones_subs:
                                phone=re.findall(r'\b[7,8,3,4,9]\d+',re.sub(r'[^\d ]','',pss).strip())
                                phone.append('')
                                if len(phone[0]) in [7,10,11]:
                                    phones[phone[0]]=pss
                            try:
                                row.append(';'.join(list(phones.keys())))
                            except:
                                row.append('')
                            try:
                                row.append(json.dumps(phones,ensure_ascii=False))
                            except:
                                row.append('')
                        except:
                            row.append('')
                            row.append('')
                        #<time_monitor>
    #                    elepsed_time['Phones']=elepsed_time.get('Phones',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
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
                        #<time_monitor>
    #                    elepsed_time['INN\KPP']=elepsed_time.get('INN\KPP',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        try:
                            s=text.split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split(' ')[0]
                            if '/' in s and 'КПП' in s:
                                s=text.split('ОГРН')[-1].replace('-','').replace(')','').replace(':','').replace('ИП','').strip().split('/')[1].split(' ')[1]
                            row.append(s)                    
                        except:
                            row.append('')
                        #<time_monitor>
    #                    elepsed_time['OGRN']=elepsed_time.get('OGRN',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
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
                        #<time_monitor>
    #                    elepsed_time['BIK']=elepsed_time.get('BIK',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        try:
                            name=[]
                            try:
                                name.append(soup.find('div',{'title':'Название'}).text)
                            except:
                                pass
                            try:
                                name.append(soup(text=re.compile('©'))[0].parent.text)
                            except:
                                pass
                            try:
                                for opf in ['ЗАО','ОАО','ПАО','АО','НПАО','НАО','ООО']:
                                    name.extend(re.findall(r'{} ".*?"'.format(opf),text))
                                name.extend(re.findall(r'ИП \w*\s*\w*\s*\w*',text))
                                name.extend(re.findall(r'ИП \w*.\w*.\w*.',text))
                            except:
                                pass
                        except:
                            pass
                        finally:
                            row.append(';'.join(set(name)))
                        #<time_monitor>
    #                    elepsed_time['BIK']=elepsed_time.get('BIK',0)+(datetime.datetime.now()-start_time).total_seconds()
    #
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
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
                        #<time_monitor>
    #                    elepsed_time['ACC']=elepsed_time.get('ACC',0)+(datetime.datetime.now()-start_time).total_seconds()
    #                    
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        try:
                            row.append(';'.join(re.findall(r'[\w\.-]+@[\w\.-]+', text)))
                        except:
                            row.append('')
                        #<time_monitor>
    #                    elepsed_time['EMAIL']=elepsed_time.get('EMAIL',0)+(datetime.datetime.now()-start_time).total_seconds()
    #                    
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        row.append(crws)
                        row.append(ptws)
                        row.append(whois)
                        row.append(phonews)
                        row.append(emailws)
                        row.append('')
                        for pmnt in ['безнал','банковск','пластиков','visa','mastercard','americanexpress','master card','american express','виза','мастеркард','мастер кард','мастер-кард','кредитн','киви','paypal','scrill','qiwi','webmoney', 'пайпал','скрилл','яндекс-деньги','яндекс.деньги','веб-мани','веб мани','яндекс деньги', 'rbk money', 'рбк мани','рапида', 'w1','liqpay','ликпей','perfectmoney','перфектмани','деньги@mail.ru', 'деньги@майл.ру']:
                            try:
                                text.index(pmnt)
                                row[-1]='1'
                                break
                            except:
                                pass
                        #<time_monitor>
    #                    elepsed_time['PAY']=elepsed_time.get('PAY',0)+(datetime.datetime.now()-start_time).total_seconds()
    #                    
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        inns=[]
                        for n in [s for s in re.sub('\D',' ',text).split(' ') if s != '']:
                            if check_inn(n):
                                inns.append(n)
                        row.append(';'.join(inns))
                        #<time_monitor>
    #                    elepsed_time['INN VALID']=elepsed_time.get('INN VALID',0)+(datetime.datetime.now()-start_time).total_seconds()
    #                    
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                        ogrns=[]
                        for n in [s for s in re.sub('\D',' ',text).split(' ') if s != '']:
                            if check_ogrn(n):
                                ogrns.append(n)
                        row.append(';'.join(ogrns))
                        data.append(row)
                        #<time_monitor>
    #                    elepsed_time['OGRN VALID']=elepsed_time.get('OGRN VALID',0)+(datetime.datetime.now()-start_time).total_seconds()
    #                    
    #                    start_time=datetime.datetime.now()
                        #</time_monitor>
                    except Exception as e:
                        print('Error: '+str(e))
            except Exception as e:
                print('Error: '+str(e))
        else:
            row=[]
            row.append(sweb)
            row.append(inp[1])
            row.append(main_content)
            row.append(web)
            row.append(title)
            row.append(meta_descr)
            row.append(meta_kw)
            row.extend(['']*18)
            row.append(crws)
            row.append(ptws)
            row.append(whois)
            row.append(phonews)
            row.append(emailws)
            row.append('')
            row.append('')
            row.append('')
            data.append(row)

#%%
if __name__ == '__main__':
    start_time=datetime.datetime.now()
    
    tid=start_time.strftime('%d%m%y_%H%M%S')
    output_filename='ecom_res_'+tid
    
    ecom_logger(tid,'START')
    
    try:
        webs=pd.read_csv('ecom_test_sample.csv',encoding='1251', sep=';')
    except:
        ecom_logger(tid,'ERROR WITH READING DOMAINS')
        sys.exit('FATAL ERROR')
    try:
        webs=webs.fillna('')
        
        if webs.shape[1] == 1:
            webs['дата']=''
        
        webs.columns=['домен','дата']
        #webs['дата']=webs['дата'].apply(lambda x: x.strftime('%d.%m.%Y'))
        webs['домен']=webs['домен'].replace({'https':'','http':'',':':'','/':'','www.':''},regex=True)
    except:
        ecom_logger(tid,'ERROR WITH PREFORMATTIG DOMAINS')
        sys.exit('FATAL ERROR')
    try:
        l=webs[['домен','дата']].values.tolist()
        n_chunks=50
        chunks=[l[i::n_chunks] for i in range(n_chunks)]
    except:
        ecom_logger(tid,'ERROR WITH CHUNKIFING')
        sys.exit('FATAL ERROR')        
        
        ecom_logger(tid,'RECEIVED FILE WITH {} DOMAINS. CHUNKED TO {} BY {}'.format(str(webs.shape[0]),str(n_chunks),str(len(chunks[0]))))
        
        #<time_monitor>
        #elepsed_time={}
        #</time_monitor>
        
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
    
        for f in [f for f in os.listdir('ecomlog') if tid in f]:
            os.remove('/ecomlog/'+f)
    #%%      
        ecom_logger(tid,'DATA COLLECTED. ELAPSED TIME {}'.format(str(datetime.datetime.now()-start_time)))
        
        writer = pd.ExcelWriter('ecom_temp.xlsx',options={'strings_to_urls': False})
        data.to_excel(writer,index=None)
        writer.close()
        data.columns=['In_Web','In_RegDate','MainContent','Out_Web','<Title>','<Description>','<Keywords>','LinkType','Link','VK','OK','Facebook','Twitter','Instagram','YouTube','Phones','PhonesLabels','INN','KPP','OGRN','BIK','NAME','CS','RS','Email','DomainRegDate','DomainExpiryDate','WHOIS','WHOIS_PHONE','WHOIS_EMAIL','Payment','INNS','OGRNS']
        data=data[['In_Web','Out_Web', 'MainContent', '<Title>','<Description>','<Keywords>','LinkType','Link','NAME','INN','KPP','OGRN','BIK','CS','RS','Phones','PhonesLabels','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','In_RegDate','DomainRegDate','DomainExpiryDate','Payment','WHOIS','WHOIS_PHONE','WHOIS_EMAIL', 'INNS','OGRNS']]
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
        
        first_attr=['Компания','О компании','Контакты','Контактная информация','Контакты и реквизиты']
        
        data['Аттрибут']='2'
        
        for i in data.loc[data['LinkType'].isin(first_attr)].index:
            data=data.set_value(i,'Аттрибут','1')
        for i in data.loc[data['LinkType']==''].index:
            data=data.set_value(i,'Аттрибут','')        
        
        writer = pd.ExcelWriter(output_filename+'_new.xlsx',options={'strings_to_urls': False})
        data.to_excel(writer,index=None)
        writer.close()
        
        data=data.drop(['Аттрибут'],axis=1)
        
        res=pd.DataFrame() 
        
        for n,i in enumerate(data['In_Web'].drop_duplicates().values.ravel()):
            sdf=data.loc[data['In_Web']==i].copy()
            lll={}
            for lt,ll in zip(sdf['LinkType'].values.ravel(),sdf['Link'].values.ravel()):
                lll[lt]=ll
            for col in ['In_Web','In_RegDate', 'MainContent', 'Out_Web','<Title>','<Description>','<Keywords>','DomainRegDate','DomainExpiryDate','WHOIS','WHOIS_PHONE','WHOIS_EMAIL']:
                res=res.set_value(n,col,sdf[col].values.ravel()[0])
            res=res.set_value(n,'Links',str(lll))
            for col in ['INN','KPP','OGRN','BIK','CS','RS','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','Payment']:
                res=res.set_value(n,col,sdf.loc[sdf[col].apply(len)==sdf[col].apply(len).max()][col].values.ravel()[0])        
            res=res.set_value(n,'INNS',';'.join(list(sdf['INNS'].values.ravel())))
            res=res.set_value(n,'OGRNS',';'.join(list(sdf['OGRNS'].values.ravel())))
            res=res.set_value(n,'NAME',';'.join(set(list(sdf['NAME'].values.ravel()))))
            res=res.set_value(n,'Phones',';'.join(set(list(sdf['Phones'].values.ravel()))))
            sdf_phones={}
            [sdf_phones.update(json.loads(psdf)) for psdf in sdf['PhonesLabels'].values if psdf != '']
            res=res.set_value(n,'PhonesLabels',json.dumps(sdf_phones,ensure_ascii=False))
        
        social_networks={'VK':'vk.com','OK':'ok.ru','Facebook':'facebook.com','Twitter':'twitter.com','Instagram':'instagram.com','YouTube':'youtube.com'}
        for s in ['VK', 'OK', 'Facebook', 'Twitter', 'Instagram']:
            res[s]=res[s].apply(lambda x: ';'.join(set([re.findall(r'^|(\b|http(\b|s)://)(\b|www.)({}/\w*)'.format(social_networks[s]),snl)[-1][-1] for snl in x.split(';')])))
        res['YouTube']=res['YouTube'].apply(lambda x: ';'.join(set([re.findall(r'^|(\b|http(\b|s)://)(\b|www.)({}/\w*/\w*)'.format(social_networks[s]),snl)[-1][-1] for snl in x.split(';')])))
        
        res['INNS']=res['INNS'].apply(lambda x: ';'.join(set([s.strip() for s in x.split(';') if s!=''])))
        res['OGRNS']=res['OGRNS'].apply(lambda x: ';'.join(set([s.strip() for s in x.split(';') if s!=''])))
        res['NAME']=res['NAME'].apply(lambda x: ';'.join(set([re.sub(r'20\d\d(| )-(| )20\d\d','',s).replace('©','').strip() for s in x.split(';') if s!=''])))
        res['Phones']=res['Phones'].apply(lambda x: ';'.join(set([s.strip() for s in x.split(';') if s!=''])))
        res=res[['In_Web','Out_Web', 'MainContent','<Title>','<Description>','<Keywords>','Links','NAME','INN','KPP','OGRN','BIK','CS','RS','Phones','PhonesLabels','Email','VK','OK','Facebook','Twitter','Instagram','YouTube','In_RegDate','DomainRegDate','DomainExpiryDate','Payment','INNS','OGRNS','WHOIS','WHOIS_PHONE','WHOIS_EMAIL']]
        
        writer = pd.ExcelWriter(output_filename+'.xlsx',options={'strings_to_urls': False})
        res.to_excel(writer,index=None)
        writer.close()
        
        ecom_logger(tid,'DATA FORMATTED. ELAPSED TIME {}'.format(str(datetime.datetime.now()-start_time)))
        
        try:
            send_mail('studtosber@gamil.com', 'ECOM', 'Result', [output_filename+'.xlsx'])
        except:
            ecom_logger(tid,'ERROR WITH SENDIG RESULT')
            sys.exit('FATAL ERROR') 
        
        #max_row=res.shape[0]
        #for dn in webs.loc[~webs['домен'].isin(res['In_Web'].values.ravel())]['домен'].values:
        #    res=res.set_value(max_row,'In_Web',dn)
        #    max_row+=1
        #%%
        #<time_monitor>
        #elepsed_time['Post edit']=elepsed_time.get('Post edit',0)+(datetime.datetime.now()-start_time).total_seconds()
        #elpsd_tm=(datetime.datetime.now()-general_start_time).total_seconds()
        #time_df=pd.DataFrame([elepsed_time]).T
        #time_df[1]=time_df[0].apply(lambda x: x*100/elpsd_tm)
        #</time_monitor>

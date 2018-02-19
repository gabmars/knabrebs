import requests 
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

months={'августа': '08',
 'апреля': '04',
 'декабря': '12',
 'июля': '07',
 'июня': '06',
 'марта': '03',
 'мая': '05',
 'ноября': '11',
 'октября': '10',
 'сентября': '09',
 'февраля': '02',
 'января': '01'}

begin_date=datetime.datetime.strptime('01.01.2018','%d.%m.%Y')
end_date=datetime.datetime.today()

head1={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'13104',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'se.fedresurs.ru',
'Origin':'https://se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/Messages',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

head2={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/Messages',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

msg_head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection':'keep-alive',
'Host':'se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/messages/IsSearching',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}


url1='https://se.fedresurs.ru/Messages'
url2='https://se.fedresurs.ru/messages/IsSearching'

df=pd.DataFrame()
i=0
for d in range((end_date-begin_date).days):
    data={
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE':'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',
        '__VIEWSTATEGENERATOR':'F8CFDE04',
        '__EVENTVALIDATION':'2F6jAY9uzBTR40IbkeQyy655o+9U3PVs6MRatJpFaLT7yVIeZPMNTpcct235LC8XXiYlWOvw1bZlgVtk2JUnBuhi24Y16cc7hOuljjrA9RxpVWAeo3BGEuUSyJamU8XcgMVmk045521Y5ZR85zU5leaXv23C33WMp7Zg5HDU/VOxR1nnBTClhJh5GzJhZ1Kr3yCyabFDqoNzIOhrM1RbUi5s4BLq2gdlUxnx8acypdHrSNfU8oTZEbR1Nc0kyt/XJsYOxOZJwJ1UyuEkq2fag3DYSyZcgWT/IFuHadj5wf8SbSPpa981lwfHPRDzNJma2YdwRkPOkfS/O1Hz9NQk3C/SvlPXG9qWD6MwLsskh+sgU8GNWwizgny/ENib88WcDVsSslQmpyeCGF2AZqcPQGhjy9Hm35U5LlHeYN0h/KT87druuUARjH/6J6g2BU0ERJop+s/JPg2nrYTDAkTq/DieuDMf97t4/qnXMcooTVo4YWn91V+AT1p3pO+L7faumwAI+ejDwpXh86srLbCqdC+zjaHA/0OddTgmCIB9hIUJBMe5YZkQZ0QfrhotWe5QLAyxt0xmczC7RiA/TYPqLPJMQXj54aFmzH6EBRtvjd8mf7r0/N5QHFVLGf5j94GIOWubVLb6ZEZjtABhhfkds+3WD9q+2TWMUjbkPoOiyirWb5w/8BjWqnjM8pc+3XipYy9xEnUh/o5QYujKQPCfi49g1L1vGB1V1hrOjFWGNwqQIfaOwqaEExuswRLa93xSjxJexVSZKTApZmMqTOlPZXoG64RJIGY81+ubbPfNHQCBMNJv2MJbInW80riboJDN4Mr8RBLDZKMTw8ED4Qx69z0t/hCotnE6XK9io7nXkxsJ690HnwoiPNQA6jBqRW4Y5WDfHDuWZhi4Eh8izS1viSHLtkwyVrVGlEOZJrqWPzKHPdgXI5tF6NKZdDisV8AHabjV/N7gEIDrhYIg9r7QXP7uhkMMfAz9b3jDWiCH/5SDKtZn27udiia++or0cxIvFcAHy8MzIJb1CHDj2juh+3udRV0MXqRezdD+D/iXMbltRr9uMzbMdXcDpvdW453iTHaIof4325WCnpkNXeOmTo6th3a0rdSPENdPNm2RJnH8dY5nstATOUSuy4A/a9Lx+ayYZud5CyG1oo0dhTMGWs15drrHWgE4+G44+ElwJg1z/HS2qGRYBVdvJcdpWIYkfYJ8FA==',
        'ctl00$tbCompanySearch':'',
        'ctl00$MainContent$sfMessageType$txtObjectName':'Сообщение о выпуске независимой гарантии',
        'ctl00$MainContent$sfMessageType$hfIdObject':'IssueIndependentGuarantee',
        'ctl00$MainContent$sfMessageType$hfAdditionalInfo':'',
        'ctl00$MainContent$cbShowForeignSystemMessages':'on',
        'ctl00$MainContent$sfCompanySelector$txtObjectName':'',
        'ctl00$MainContent$sfCompanySelector$hfIdObject':'',
        'ctl00$MainContent$sfCompanySelector$hfAdditionalInfo':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$txtObjectName':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$hfIdObject':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$hfAdditionalInfo':'',
        'ctl00$MainContent$sfAppraiser$txtObjectName':'',
        'ctl00$MainContent$sfAppraiser$hfIdObject':'',
        'ctl00$MainContent$sfAppraiser$hfAdditionalInfo':'',
        'ctl00$MainContent$sfPerson$txtObjectName':'',
        'ctl00$MainContent$sfPerson$hfIdObject':'',
        'ctl00$MainContent$sfPerson$hfAdditionalInfo':'',
        'ctl00$MainContent$sfNonResidentCompany$txtObjectName':'',
        'ctl00$MainContent$sfNonResidentCompany$hfIdObject':'',
        'ctl00$MainContent$sfNonResidentCompany$hfAdditionalInfo':'',
        'ctl00$MainContent$dpBeginPublishDate$txtDate':(begin_date+datetime.timedelta(d)).strftime('%d.%m.%Y'),
        'ctl00$MainContent$dpEndPublishDate$txtDate':(begin_date+datetime.timedelta(d)).strftime('%d.%m.%Y'),
        'ctl00$MainContent$tbMessageNumber':'',
        'ctl00$MainContent$btnSearch':'Поиск',
        'ctl00$MainContent$ucMonitoringControl$txtEmail':'',
        'ctl00$MainContent$ucMonitoringControl$txtPassword':''}
    proxies={'http':'92.126.153.83:8080'}
    session=requests.Session()
    session.proxies=proxies
    for j in range(9):
        res1=session.post(url2,headers=head1,data=data)
        soup=BeautifulSoup(res1.text,'lxml')
        links=soup.find_all('div',{'class':'listItem'})
        for link in links:
            sss=None
            print(i)
            msg_url='https://se.fedresurs.ru'+link['onclick'][len(" window.location.assign('"):link['onclick'].find("');")]
            msg=session.get(msg_url,headers=msg_head)
            msg_soup=BeautifulSoup(msg.text,'lxml')
            try:
                substr1=msg_soup.find('div',{'id':'content'}).find('td',{'data-element-type':'page-content'}).find('div').find_all('div')[0].text.replace('\n',' ').replace('\r',' ').replace('\xa0',' ').replace('№','').strip()
                df=df.set_value(i,'Номер',substr1.split()[1])
                df=df.set_value(i,'Дата публикации',substr1.split()[3])
            except:
                pass
            try:
                trs=msg_soup.find('div',{'id':'content'}).find('td',{'data-element-type':'page-content'}).find('div').find_all('div')[4].find_all('tr')
                try:
                    df=df.set_value(i,'Тип сообщения',[ss for ss in trs[0].text.strip().split('  ') if ss!=''][1])
                except:
                    pass
                try:
                    df=df.set_value(i,'Гарант',[ss for ss in trs[1].text.strip().split('  ') if ss!=''][1])
                except:
                    pass
                try:
                    sss=[ss for ss in trs[1].text.strip().split('  ') if ss!=''][2]
                except:
                    pass
                else:
                    try:
                        df=df.set_value(i,'Гарант_ИНН',sss[len('(ИНН: '):sss.find(',')])
                    except:
                        pass
                    try:
                        df=df.set_value(i,'Гарант_ОГРН',sss[sss.find(',')+len(' ОГРН: '):sss.find(')')].strip())
                    except:
                        pass
                try:
                    sss=[ss for ss in trs[2].text.strip().split('  ') if ss!=''][1]
                    if 'ИНН' in sss:
                        df=df.set_value(i,'Принципал',sss[:sss.find(' (ИНН: ')])
                        df=df.set_value(i,'Принципал_ИНН',sss[sss.find(' (ИНН: ')+len(' (ИНН: '):sss.find(', ОГРНИП:')])
                        df=df.set_value(i,'Принципал_ОГРН',sss[sss.find(', ОГРНИП: ')+len(', ОГРНИП: '):sss.find(')')])
                    else:
                        df=df.set_value(i,'Принципал',sss)
                except:
                    pass
                try:
                    sss=[ss for ss in trs[2].text.strip().split('  ') if ss!=''][2]
                except:
                    pass
                else:
                    if ', Аналог ИНН: ' in sss:
                        df=df.set_value(i,'Принципал_ИНН',sss[sss.find(', Аналог ИНН: ')+len(', Аналог ИНН: '):sss.find(')')])
                    else:
                        try:
                            df=df.set_value(i,'Принципал_ИНН',sss[len('(ИНН: '):sss.find(',')])
                        except:
                            pass
                        try:
                            df=df.set_value(i,'Принципал_ОГРН',sss[sss.find(',')+len(' ОГРН: '):sss.find(')')].strip())
                        except:
                            pass
                try:
                    df=df.set_value(i,'Бенефициар',trs[6].find('td').text)
                except:
                    pass
                try:
                    sss=trs[6].find_all('td')[1].text.split()
                except:
                    pass
                else:
                    if 'Аналог' in sss:
                        df=df.set_value(i,'Бенефициар_ИНН',sss[-1])
                    else:
                        try:
                            df=df.set_value(i,'Бенефициар_ИНН',sss[1])
                        except:
                            pass
                        try:
                            df=df.set_value(i,'Бенефициар_ОГРН',sss[3])
                        except:
                            pass
                try:
                    df=df.set_value(i,'Номер гарантии',trs[8].find_all('td')[1].text)
                except:
                    pass
                try:
                    df=df.set_value(i,'Дата выдачи',trs[9].find_all('td')[1].text)
                except:
                    pass
                try:
                    df=df.set_value(i,'Дата начала действия',trs[10].find_all('td')[1].text)
                except:
                    pass
                try:
                    sss=trs[11].find_all('td')[1].text
                    sss=sss[sss.find(' по «')+len(' по «'):sss.find(' года')].replace('»','').split(' ')
                    sss='.'.join([sss[0],months[sss[1]],sss[2]])
                    df=df.set_value(i,'Дата завершения действия',sss)
                except:
                    try:
                        df=df.set_value(i,'Дата завершения действия',trs[11].find_all('td')[1].text.strip())                
                    except:
                        pass                
                try:
                    sss=trs[13].find_all('td')[1].text
                    df=df.set_value(i,'Ссылка на торги на ЭТП',sss[sss.find('№')+1:sss.find('от')].strip())
                except:
                    pass
                try:
                    df=df.set_value(i,'Описание основного обязательства',trs[14].find_all('td')[1].text)
                except:
                    pass
                try:
                    df=df.set_value(i,'Сумма',trs[16].find_all('td')[1].text)
                except:
                    pass
                try:
                    df=df.set_value(i,'Неизменяемая сумма',trs[17].find_all('td')[1].text)
                except:
                    pass
                try:
                    df=df.set_value(i,'Ссылка',link['onclick'][len(" window.location.assign('"):link['onclick'].find("');")])
                except:
                    pass
            except:
                pass  
            i+=1
        try:
            sss1=soup.find('input',{'id':'__VIEWSTATE'})['value']
            sss2=soup.find('input',{'id':'__EVENTVALIDATION'})['value']
        except:
            sss1=soup.text[soup.text.find('__VIEWSTATE|')+len('__VIEWSTATE|'):]
            sss1=sss1[:sss1.find('|')]
            sss2=soup.text[soup.text.find('__EVENTVALIDATION|')+len('__EVENTVALIDATION|'):]
            sss2=sss2[:sss2.find('|')]
        data={
        'ctl00$ScriptManager1':'ctl00$MainContent$ctl12|ctl00$MainContent$ucBottomDataPager$ctl00$ctl0{}'.format(j+1),
        'ctl00$tbCompanySearch':'',
        'ctl00$MainContent$sfMessageType$txtObjectName':'Сообщение о выпуске независимой гарантии',
        'ctl00$MainContent$sfMessageType$hfIdObject':'IssueIndependentGuarantee',
        'ctl00$MainContent$sfMessageType$hfAdditionalInfo':'',
        'ctl00$MainContent$cbShowForeignSystemMessages':'on',
        'ctl00$MainContent$sfCompanySelector$txtObjectName':'',
        'ctl00$MainContent$sfCompanySelector$hfIdObject':'',
        'ctl00$MainContent$sfCompanySelector$hfAdditionalInfo':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$txtObjectName':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$hfIdObject':'',
        'ctl00$MainContent$sfIndividualEntrepreneur$hfAdditionalInfo':'',
        'ctl00$MainContent$sfAppraiser$txtObjectName':'',
        'ctl00$MainContent$sfAppraiser$hfIdObject':'',
        'ctl00$MainContent$sfAppraiser$hfAdditionalInfo':'',
        'ctl00$MainContent$sfPerson$txtObjectName':'',
        'ctl00$MainContent$sfPerson$hfIdObject':'',
        'ctl00$MainContent$sfPerson$hfAdditionalInfo':'',
        'ctl00$MainContent$sfNonResidentCompany$txtObjectName':'',
        'ctl00$MainContent$sfNonResidentCompany$hfIdObject':'',
        'ctl00$MainContent$sfNonResidentCompany$hfAdditionalInfo':'',
        'ctl00$MainContent$dpBeginPublishDate$txtDate':(begin_date+datetime.timedelta(d)).strftime('%d.%m.%Y'),
        'ctl00$MainContent$dpEndPublishDate$txtDate':(begin_date+datetime.timedelta(d)).strftime('%d.%m.%Y'),
        'ctl00$MainContent$tbMessageNumber':'',
        'ctl00$MainContent$ucMonitoringControl$txtEmail':'',
        'ctl00$MainContent$ucMonitoringControl$txtPassword':'',
        '__EVENTTARGET':'ctl00$MainContent$ucBottomDataPager$ctl00$ctl0{}'.format(j+1),
        '__EVENTARGUMENT':'',
        '__VIEWSTATE':sss1,
        '__VIEWSTATEGENERATOR':'F8CFDE04',
        '__EVENTVALIDATION':sss2,
        '__ASYNCPOST':'true'}  
df=df.drop_duplicates()

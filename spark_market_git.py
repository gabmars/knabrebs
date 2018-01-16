import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import os

head_post={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'41',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'www.spark-marketing.ru',
'Origin':'http://www.spark-marketing.ru',
'Referer':'http://www.spark-marketing.ru/Auth/Login',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
head_search={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Host':'www.spark-marketing.ru',
'Referer':'http://www.spark-marketing.ru/Purchases/Search',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

head_create={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Content-Length':'478',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.spark-marketing.ru',
'Origin':'http://www.spark-marketing.ru',
'Referer':'http://www.spark-marketing.ru/Purchases/Search',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'x-ms-request-id':'m8OK5',
'x-ms-request-root-id':'OEaNC',
'X-Requested-With':'XMLHttpRequest'}

head_wait={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Content-Length':'45',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.spark-marketing.ru',
'Origin':'http://www.spark-marketing.ru',
'Referer':'http://www.spark-marketing.ru/Purchases/Search',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'x-ms-request-id':'/mz7g',
'x-ms-request-root-id':'OEaNC',
'X-Requested-With':'XMLHttpRequest'}

report_generate_head={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Content-Length':'69',
'Content-Type':'application/json; charset=UTF-8',
'Host':'www.spark-marketing.ru',
'Origin':'http://www.spark-marketing.ru',
'Referer':'',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'x-ms-request-id':'/p1mu',
'x-ms-request-root-id':'E3Djq',
'X-Requested-With':'XMLHttpRequest'}

get_report_head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Host':'www.spark-marketing.ru',
'Referer':'',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


dirct='C:\\Users\\Марсель Габдулханов\\Documents\\sber\\spark_marketing'
#%%

url_post='http://www.spark-marketing.ru/Auth/Login'
data={'UserName':'','Password':''}
session=requests.Session()
login_in=session.post(url_post, data=data, headers=head_post)

search_url='http://www.spark-marketing.ru/Purchases/Search'
search_resp=session.get(search_url,headers=head_search)
search_soup=BeautifulSoup(search_resp.text,'lxml')

#%%

search_data='SearchParams.SearchResultsAggregationMode=Counts&SearchParams.SearchResultsOrderMode=ActivationDate&SearchParams.SearchResultsOrderDirectMode=Desc&SearchParams.ActivationDateBack=Yesterday&SearchParams.DirectDealTypesIds=1&SearchParams.PublicationTypesIds=1&SearchParams.CustomersIdsSearchFilterMode=Or&SearchParams.SuppliersIdsSearchFilterMode=Or&SearchParams.ClassifiersSearchFilterMode=Or&SearchParams.OrganizersIdsSearchFilterMode=Or'
create_search_url='http://www.spark-marketing.ru/Purchases/CreateSearch'
create_search_resp=session.post(create_search_url,headers=head_create,data=search_data)
create_search_soup=BeautifulSoup(create_search_resp.text,'lxml')
vals=json.loads(create_search_soup.find('p').text)
wait_data='workRequestId={}&userRequestId={}'.format(str(vals['WorkRequestId']),str(vals['UserRequestId']))
wait_url='http://www.spark-marketing.ru/Purchases/WaitForCompleteRequest'
wait_resp=session.post(wait_url,headers=head_wait,data=wait_data)
result_url='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
report_generate_head['Referer']='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
get_report_head['Referer']='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
result_resp=session.get(result_url,headers=head_search)
result_soup=BeautifulSoup(result_resp.text,'lxml')

regions=[[r['data-id'],r.find('em').text.replace(u'\xa0','')] for r in result_soup.find('ul',{'data-ns':'SearchParams.DeliveriesIds'}).find_all('li') if r['data-id']!='-1']
regions_for_search=[]
cs=0
sreg=''
for reg in regions:
    if int(reg[1])+cs>10000:
        regions_for_search.append(sreg[:-1])
        sreg=''
        cs=0
    else:
        sreg+='{}%2FOKATO,'.format(reg[0])
        cs+=int(reg[1])
for region in regions_for_search:
    search_data='SearchParams.SearchResultsAggregationMode=Counts&SearchParams.SearchResultsOrderMode=ActivationDate&SearchParams.SearchResultsOrderDirectMode=Desc&SearchParams.ActivationDateBack=Yesterday&SearchParams.DirectDealTypesIds=1&SearchParams.PublicationTypesIds=1&SearchParams.CustomersIdsSearchFilterMode=Or&SearchParams.SuppliersIdsSearchFilterMode=Or&SearchParams.DeliveriesIds={}&SearchParams.ClassifiersSearchFilterMode=Or&SearchParams.OrganizersIdsSearchFilterMode=Or'.format(region)
    
    create_search_resp=session.post(create_search_url,headers=head_create,data=search_data)
    create_search_soup=BeautifulSoup(create_search_resp.text,'lxml')
    
    vals=json.loads(create_search_soup.find('p').text)
    
    wait_data='workRequestId={}&userRequestId={}'.format(str(vals['WorkRequestId']),str(vals['UserRequestId']))
    
    wait_resp=session.post(wait_url,headers=head_wait,data=wait_data)
    
    result_url='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
    report_generate_head['Referer']='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
    get_report_head['Referer']='http://www.spark-marketing.ru/Purchases/Search?tinyUrl={}'.format(str(vals['tinyUrl']))
    result_resp=session.get(result_url,headers=head_search)
    result_soup=BeautifulSoup(result_resp.text,'lxml')
    
    generate_report_utl='http://www.spark-marketing.ru/Purchases/GenerateSearchReport'
    generate_report_data=json.dumps({"userRequestId":str(vals['UserRequestId']),"workRequestId":str(vals['WorkRequestId']),"selected":[]})
    
    generate_report_resp=session.post(generate_report_utl, headers=report_generate_head,data=generate_report_data)
    generate_report_soup=BeautifulSoup(generate_report_resp.text,'lxml')
    reportId=json.loads(generate_report_soup.find('p').text)['reportId']
    
    time.sleep(60)
    
    get_reports_url='http://www.spark-marketing.ru/User/Reports'
    get_reports_resp=session.get(get_reports_url,headers=get_report_head)
    get_reports_soup=BeautifulSoup(get_reports_resp.text,'lxml')

    report_resp=session.get('http://www.spark-marketing.ru{}'.format(get_reports_soup.find('tr',{'data-id':reportId}).find('a')['href']))
    with open(dirct+'\\temp\\{}.xlsx'.format(region), 'wb') as f:
            f.write(report_resp.content)
            f.close()

data=pd.DataFrame()
for f in os.listdir(dirct+'\\temp'):
    df=pd.read_excel(dirct+'\\temp\\'+f,'Результаты поиска',skiprows=1)
    df=df[['ИНН', 'Стоимость\n(руб.)', 'Реестровый номер', 'Сфера деятельности', 
          'Наименование публикации', 'Unnamed: 7', 'Unnamed: 10', 'Unnamed: 12', 
          'Поставщик', 'Unnamed: 20', 'Unnamed: 22', 'Unnamed: 23']]
    df.columns=['ИНН', 'Стоимость', 'Реестровый номер', 'Сфера деятельности', 
          'Наименование публикации', 'Регион поставки', 'Дата окончания приема заявок / Дата завершения контракта', 
          'Дата  окончания проведения торгов', 
          'Поставщик', 'Тип торгов', 'Обеспечение заявки', 'Обеспечение контракта']
    df=df.loc[df['Поставщик'].isnull()]
    df=df.drop('Поставщик',axis=1)
    df=df.dropna(subset=['ИНН'])
    df=df.dropna(subset=['Стоимость'])
    df=df.loc[df['Сфера деятельности']!='Неизвестно']
    df=df.loc[df['Тип торгов']!='Неизвестно']
    data=pd.concat([data,df],ignore_index=True)

data.to_excel(dirct+'\\purchases.xlsx',index=None)
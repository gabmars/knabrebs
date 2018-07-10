import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

g45=['Бабайлова Маргарита Леонидовна', 'Бабикова Евгения Витальевна',
   'Бармин Михаил Антонович', 'Березовик Екатерина Игоревна', 
   'Водяный Михаил Викторович','Высокий Лев Олегович',
   'Габдулханов Марсель Васимович','Жидков Илья Александрович', 
   'Зубарева Марина Николаевна', 'Кабанов Евгений Алексеевич', 
   'Кичигина Татьяна Сергеевна','Комлева Юлия Владимировна', 
   'Котов Иван Юрьевич', 'Миронова Елена Андреевна',
   'Никитина Наталья Хозиевна', 'Патракова Екатерина Сергеевна',
   'Секлецов Даниил Иванович', 'Татарченков Андрей Павлович',
   'Тесленко Денис Алексеевич', 'Цыпаев Владимир Николаевич',
   'Шубин Дмитрий Игоревич','Сычева Дарья Игоревна']

head1={
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Host': 'urfu.ru',
'Referer': 'https://urfu.ru/ru/alpha/full/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}

head2={
'Accept': 'text/html, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Host': 'urfu.ru',
'Referer': 'https://urfu.ru/ru/alpha/full/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}

data=pd.DataFrame()

for n in range(1,34):
    if n in [11,28,30]:
        continue
    print(n)
    res=requests.get('https://urfu.ru/api/ratings/alphabetical/1/{}/'.format(n),headers=head1)
    res=requests.get('https://urfu.ru'+json.loads(res.text)['url'],headers=head2)
    soup=BeautifulSoup(res.text,'lxml')
    table=soup.find('table',{'class':'alpha supp table-header'})
    if table:
        prt=1
        for tr in table.find_all('tr'):
            if tr.find('td',{'colspan':'3'}):
                row=[]
                nr=tr.find_all('td',rowspan=True)
                if nr:
                    name=nr[0].text
                    reg_num=nr[1].text
                tds=tr.find_all('td',rowspan=False)
                if len(tds) == 10:
                    row.append(name)
                    row.append(reg_num)
                for td in tds:
                    row.append(td.text)
                if data.shape[0]>0:
                    if data.tail(1).values[0][0]==row[0]:
                        prt+=1
                    else:
                        prt=1
                row.append(prt)
                data=data.append([row],ignore_index=True)
                
        
data.columns=['Фамилия Имя Отчество','Рег.№','Состояние','Вид конкурса','Док. об образовании','Направление (специальность)','Образовательная/магистерская программа (институт/филиал)','Форма обучения','Бюджетная (контрактная) основа','Вступительные испытания по предметам','Индивидуальные достижения','Сумма конкурсных баллов','Приоритет(?)']
data=data[['Приоритет(?)','Фамилия Имя Отчество', 'Рег.№', 'Состояние', 'Вид конкурса','Док. об образовании', 'Направление (специальность)','Образовательная/магистерская программа (институт/филиал)','Форма обучения', 'Бюджетная (контрактная) основа','Вступительные испытания по предметам', 'Индивидуальные достижения','Сумма конкурсных баллов']]
data=data.loc[data['Направление (специальность)']=='09.04.02 Информационные системы и технологии (вступительный экзамен по программе №358)']
data.to_excel('mag_list.xlsx',index=None)
#data=data.loc[~data['Фамилия Имя Отчество'].isin(g45)]
#data.to_excel('mag_list_not_g45.xlsx',index=None)

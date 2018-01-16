import requests
from bs4 import BeautifulSoup
import pandas as pd

df=pd.DataFrame()
url='http://www.consultant.ru/document/cons_doc_LAW_148920/af6ff7978452eadf512aa7dca1a552e7b41e6806/'
resp=requests.get(url)
soup=BeautifulSoup(resp.text,'lxml')
links=[l.next.attrs['href'] for l in soup.find_all('li')]
i=0
for l in links:
    kbk=requests.get('http://www.consultant.ru'+l)
    tables=BeautifulSoup(kbk.text,'lxml').find_all('table',{'cellpadding':"0",'cellspacing':"0",'border':"0",'class':"dyntable",'start':"34170",'end':"39202"})
    for t in tables[1:]:
        try:
            if l == links[len(links)-1]:
                adm=tables[0].find_all('span',{'class':'blk'})[1].text
                code='000'+t.find_all('span',{'class':'blk'})[1].text
            else:
                adm=tables[0].find_all('span',{'class':'blk'})[2].text
                code=t.find_all('span',{'class':'blk'})[0].text+' '+t.find_all('span',{'class':'blk'})[1].text
            code=''.join(code.split(' '))
            desc=t.find_all('span',{'class':'blk'})[2].text
            if 'исключено' in desc.lower():
                raise Exception
            if ('\xa0' == code) or ('\xa0\xa0' == code) or ('\xa0' == desc) or ('\xa0\xa0' == desc):
                raise Exception
            df=df.set_value(i,'ADMIN',adm)
            df=df.set_value(i,'ADM_CODE',code[:3])
            df=df.set_value(i,'CODE',code[3:])
            df=df.set_value(i,'DESCRIPTION',desc)
        except:
            continue
        i+=1
df=df.replace({'<1>':''},regex=True)

df1=pd.DataFrame()
url=['http://www.consultant.ru/document/cons_doc_LAW_148920/93bdca826fcae07da0ead27a8db14279be22dd4a/','http://www.consultant.ru/document/cons_doc_LAW_148920/9c53c5fbfe15c3403673004c6c14c14c0d6b70a1/']
i=0
for u in url:
    resp=requests.get(u)
    soup=BeautifulSoup(resp.text,'lxml')
    links=[l.next.attrs['href'] for l in soup.find_all('li')]
    for l in links:
        kbk=requests.get('http://www.consultant.ru'+l)
        tables=BeautifulSoup(kbk.text,'lxml').find_all('table',{'cellpadding':"0",'cellspacing':"0",'border':"0",'class':"dyntable",'start':"44794",'end':"56956"})
        for t in tables[1:]:
            try:
                if l == links[len(links)-1]:
                    adm=tables[0].find_all('span',{'class':'blk'})[1].text
                    code='000'+t.find_all('span',{'class':'blk'})[1].text
                else:
                    adm=tables[0].find_all('span',{'class':'blk'})[2].text
                    code=t.find_all('span',{'class':'blk'})[0].text+' '+t.find_all('span',{'class':'blk'})[1].text
                code=''.join(code.split(' '))
                desc=t.find_all('span',{'class':'blk'})[2].text
                if 'исключено' in desc.lower():
                    raise Exception
                if ('\xa0' == code) or ('\xa0\xa0' == code) or ('\xa0' == desc) or ('\xa0\xa0' == desc):
                    raise Exception
                df1=df1.set_value(i,'ADMIN',adm)
                df1=df1.set_value(i,'ADM_CODE',code[:3])
                df1=df1.set_value(i,'CODE',code[3:][:10]+'0000'+code[3:][14:17])
                df1=df1.set_value(i,'SUBCODE',code[3:][10:14])
                df1=df1.set_value(i,'DESCRIPTION',desc)
            except:
                continue
            i+=1
    df1=df1.replace({'<1>':''},regex=True)

for j in df.index:
    val=df1.loc[df1['CODE']==df['CODE'][j]]
    for v in val.index:
        df=df.set_value(j,str(val['SUBCODE'][v]),val['DESCRIPTION'][v].replace(df['DESCRIPTION'][j],''))
df=df.fillna('')
#%%
data=pd.DataFrame()
cols=df.columns
i=0

for k in df.index:
    for c in cols[4:]:
        if (c=='2100'):
            if df[c][k]!='':
                code2000=df[cols[1]][k]+df[cols[2]][k][:10]+c+df[cols[2]][k][14:17]
            else:
                try:
                    if code2000=='':
                        code2000=''
                except:
                    code2000=''                    
        elif (c=='3000'):
            if df[c][k]!='':
                code3000=df[cols[1]][k]+df[cols[2]][k][:10]+c+df[cols[2]][k][14:17]
            else:
                code3000=''
    for c in cols[4:]:
        if (c!='2000') and (c!='2100') and (c!='2200') and (df[c][k]!=''):
            data=data.set_value(i,cols[0],df[cols[0]][k])
            data=data.set_value(i,cols[1],df[cols[1]][k]+df[cols[2]][k])
            data=data.set_value(i,cols[3],df[cols[3]][k]+df[c][k])
            data=data.set_value(i,'1000',df[cols[1]][k]+df[cols[2]][k][:10]+c+df[cols[2]][k][14:17])
            data=data.set_value(i,'2000',code2000)
            data=data.set_value(i,'3000',code3000)
            i+=1
    del code2000
    del code3000
data.columns=['ADMIN','CODE','DESCRIPTION','MAIN_PAYMENT','PENALTY','FINE']
data=data.fillna('')
#%%
nalog=pd.read_excel('nkbk.xlsx',header=None).fillna('')
nalog=nalog.replace({'КБК 2017 - ': ''}, regex=True)
for c in nalog.columns[2:]:
    nalog[c]=nalog[c].apply(lambda x: ''.join(x.split()))
for j in nalog.index:
    nalog=nalog.set_value(j, 5, nalog[2][j][:13]+'0000'+nalog[2][j][17:])
nalog=nalog[[0,5,1,2,3,4]]
nalog.columns=['SUB_NALOG','CODE','DESCRIPTION','MAIN_PAYMENT','PENALTY','FINE']
nalog['ADMIN']='Федеральная налоговая служба'
nalog=nalog[['ADMIN','SUB_NALOG','CODE','DESCRIPTION','MAIN_PAYMENT','PENALTY','FINE']]
data=data.drop(data.loc[data['ADMIN']=='Федеральная налоговая служба'].index)
data['SUB_NALOG']=''
data=data[['ADMIN','SUB_NALOG','CODE','DESCRIPTION','MAIN_PAYMENT','PENALTY','FINE']]
data=pd.concat([data,nalog], ignore_index=True)
data['REDACTION_DATE']='16.06.2017'
data=data.sort_values('ADMIN')
data.to_excel('kbk2017.xls',index=None)
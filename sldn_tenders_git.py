import requests
import requests_ftp
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import zipfile
import json

requests_ftp.monkeypatch_session()
url=''

session=requests.Session()

auth=('','')
r1=session.list(url,auth=auth)

df=pd.DataFrame([list(filter(None,t.split(' '))) for t in r1.text.split('\r\n')])
df=df.replace({'':None})
df=df.dropna(0,'all')
df=df.fillna('')
df[4]=df[0]+' '+df[1]
df=df.drop([0,1],axis=1)
df.columns=['type/size','file','datetime']
df['datetime']=df['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%m-%d-%y %I:%M%p'))
df=df.sort_values('datetime',ascending=False)

with open('sldn_control.json') as c:
    control = json.load(c)['control']
    c.close()
    

files=df.loc[df['datetime'].apply(lambda x: x.date())==datetime.datetime.now().date()]['file'].values

#files=df.loc[df['datetime'].apply(lambda x: (x-datetime.timedelta(1)).date())>datetime.datetime.strptime(control,'%Y%m%d').date()]['file'].values

if len(files)>0:
    new_control=files[0].split('_')[0]
    if new_control != control:
        with open('sldn_control.json','w') as lock:
            json.dump({'control':new_control},lock)
            lock.close()
        zf=zipfile.ZipFile('bg.zip','w',zipfile.ZIP_DEFLATED)
        for f in files:
            print(f)
            r=session.get(url+f,auth=auth)
            with open(f, 'wb') as file:
                file.write(r.content)
                file.close()
            zf.write(f)
        zf.close()
        user=''
        server = smtplib.SMTP()
        server.connect('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(user,'')
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = ''
        msg['Subject'] = 'Bank guarantees'
        with open('bg.zip','rb') as file:
            part=MIMEApplication(file.read(),Name=f)
            part['Content-Disposition']='attachment; filename="{}"'.format('bg.zip')
            msg.attach(part)
        server.sendmail(user,[''],msg.as_string())
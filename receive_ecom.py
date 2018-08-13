import imaplib
import email
import os
import hashlib
import datetime
import sys 

def ecom_logger(message):
    print('{} {}'.format(str(datetime.datetime.now()), message))
    with open('ecom_mail_log', 'a') as file:
        file.write('{} {}'.format(str(datetime.datetime.now()), message))
        file.close()

with open('checks', 'r') as file:
    checks=file.read().split('\n')
    file.close()
try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com',993)
    imapSession.login('ecomscanner@gmail.com','EcomS123')
    imapSession.select('inbox')
except Exception as e:
    ecom_logger('ERROR WITH CONNECTING TO MAILBOX: '+str(e))
    sys.exit('FATAL ERROR') 
try:
    typ, data = imapSession.search(None, 'ALL')
except Exception as e:
    ecom_logger('ERROR WITH EXTRACTING MAILS: '+str(e))
    sys.exit('FATAL ERROR')     
    
    if typ=='OK':
        mids=data[0].split()
        for i in mids:
            try:
                typ, bmsg = imapSession.fetch(i, '(RFC822)' )
                
                if typ=='OK':    
                    for response_part in bmsg:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_string(response_part[1].decode('utf8'))
                            
                            if msg.get('Subject').upper() == 'ECOM':
                                for part in msg.walk():
                                    if part.get_content_maintype() == 'multipart':
                                        continue
                                    if part.get('Content-Disposition') is None:
                                        continue
                                    filename = part.get_filename()
                        
                                    if filename:
                                        md5=hashlib.md5()
                                        md5.update(part.get_payload(decode=True))
            
                                        if md5.hexdigest() not in checks:
                                            fp = open(filename, 'wb')
                                            fp.write(part.get_payload(decode=True))
                                            fp.close()
                                            
                                            with open('checks', 'a') as file:
                                                file.write(md5.hexdigest()+'\n')
                                                file.close()
            except Exception as e:
                ecom_logger('ERROR WITH DOWNLOADING: '+str(e))
try:
    imapSession.close()
    imapSession.logout()
except:
    pass
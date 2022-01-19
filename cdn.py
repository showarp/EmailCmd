import poplib
from email.parser import Parser
from email.header import decode_header
import base64
import os
import re
import time
def file_read(path):
	with open(path,'r') as f:
		return f.read()
def file_write(path,str):
    with open(path,'w') as f:
        f.write(str)
def emaildecode(str):
    if len(re.findall(r'(?<=B\?).*?(?=\?=)',str))>=1:
        return base64.b64decode(str.replace('=','').split('?')[-2]).decode()
    else:return str
def time_format(s):
    a=(
        re
        .findall(r'(?<=Wed,).*?(?=\+)',s)[0].strip()
        .replace('Jan','01')
        .replace('Feb','02')
        .replace('Mar','03')
        .replace('Apr','04')
        .replace('May','05')
        .replace('Jun','06')
        .replace('Jul','07')
        .replace('Aug','08')
        .replace('Sep','09')
        .replace('Oct','10')
        .replace('Nov','11')
        .replace('Dec','12')
        )
    return time.mktime(time.strptime(a,r'%d %m %Y %H:%M:%S'))
file_write(r'./config.ini',str(time.time()))
email="xxxxxxxxxxx"
#你的邮箱
pswd="xxxxxxxxxxx"
#密钥
server=poplib.POP3_SSL(host="pop.qq.com",port=995)
server.user(email)
server.pass_(pswd)
while True:
    resp, mails, octets = server.list()
    resp, lines, octets = server.retr(len(mails))
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    cmd = emaildecode(msg['Subject'])
    if re.findall(r'(?<=<).*?(?=>)',msg['From'])[0] == msg['To'] and time_format(msg['Date'])>float(file_read(r'./config.ini')):
        file_write(r'./config.ini',str(time_format(msg['Date'])))
        print(os.system(cmd))
    time.sleep(2.5)

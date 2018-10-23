#!/usr/bin/env python
#coding:utf-8
#------------------------cdn日志统计--------------------------
import sys
import os
#import pandas as pd
import commands
import time
import xlwt
import datetime
import urllib, urllib2
import smtplib
from email.Header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys
import subprocess

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

mail_host ="smtp.exmail.qq.com"
mail_user = ""
mail_postfix = ''
mail_pass = "xxx"


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
print yesterday
dateFormat = xlwt.XFStyle()
dateFormat.num_format_str = 'yyyy/mm/dd'
day = str(yesterday).replace('-','')

basepath = os.path.dirname(os.path.abspath(__file__))
dpath = '/app/data/logs/cdn'
logpath = dpath

totalpv = 0
ttoopv = 0
tredirecpv = 0
terrpv = 0

donepv = 0
toopv = 0
redirecpv = 0
errpv = 0
flag1 = "/?type=2"
flag2 = "/?type=1"

def DownloadData():
  cmd = """/usr/bin/python %s/GetDayLog.py www.xxx.cn -u xxxx -p xxxx --day %s %s""" % (basepath,day,dpath)
  status = subprocess.call(cmd,shell=True,timeout=3000)
  if status == 0:
    cmd = """gunzip %s-www.xxx.cn.gz;mv %s-www.xxx.cn %s/%s-www.xxx.cn.log""" % (day,day,dpath,day)
    status = subprocess.call(cmd,shell=True,timeout=3000)
    if status == 0:
      print "down finish:"+str(time.time())
      return True
  else:
    print "File download fail."
    return False


def GenLog():
  totalpv = 0
  ttoopv = 0
  tredirecpv = 0
  terrpv = 0

  donepv = 0
  toopv = 0
  redirecpv = 0
  errpv = 0
  flag1 = "/?type=2"
  flag2 = "/?type=1"
  for files in os.listdir(logpath):
    logfile = os.path.join(logpath,files)
    with open(logfile,'r') as fo:
      for line in fo:
        spline = line.split()
        totalpv += 1
        if spline[7] == '200':
          ttoopv += 1
        if spline[7] == '301' or spline[7] == '302':
          tredirecpv += 1
        if spline[7] == '500':
          terrpv += 1
        if flag1 in spline[3] or flag2 in spline[3] and spline[1] != "123.206.212.144":
          donepv += 1
          if spline[7] == '200':
            toopv += 1
          if spline[7] == '301' or spline[7] == '302':
            redirecpv += 1
          if spline[7] == '500':
            errpv += 1
        else:
          pass
  workbook = xlwt.Workbook(encoding='utf-8')
  booksheet1=workbook.add_sheet('落地页', cell_overwrite_ok=True)  
  booksheet2=workbook.add_sheet('完成页', cell_overwrite_ok=True)  

  booksheet1.write(0,0,'日期')
  booksheet1.write(0,1,'页面点击量')
  booksheet1.write(0,2,'成功加载量（200）')
  booksheet1.write(0,3,'重定向数')
  booksheet1.write(0,4,'服务器错误数')

  booksheet1.write(1,0,yesterday,dateFormat)
  booksheet1.write(1,1,totalpv)
  booksheet1.write(1,2,ttoopv)
  booksheet1.write(1,3,tredirecpv)
  booksheet1.write(1,4,terrpv)

  booksheet2.write(0,0,'日期')
  booksheet2.write(0,1,'页面点击量')
  booksheet2.write(0,2,'成功加载量（200）')
  booksheet2.write(0,3,'重定向数')
  booksheet2.write(0,4,'服务器错误数')

  booksheet2.write(1,0,yesterday,dateFormat)
  booksheet2.write(1,1,donepv)
  booksheet2.write(1,2,toopv)
  booksheet2.write(1,3,redirecpv)
  booksheet2.write(1,4,errpv)

  workbook.save('xxx页面数据_%s.xls' % day)


#DATA_ALL = (
#	('日期','页面点击量','成功加载量（200）','重定向数','服务器错误数'),
#	(yesterday,totalpv,ttoopv,tredirecpv,terrpv)
#	)
#DATA_DONE = (
#        ('日期','页面点击量','成功加载量（200）','重定向数','服务器错误数'),
#        (yesterday,donepv,toopv,redirecpv,errpv)
#        )

#for i, row in enumerate(DATA_ALL):
#	for j,col in enumerate(row):
#          booksheet1.write(i,j,col)


#for i, row in enumerate(DATA_DONE):
#        for j,col in enumerate(row):
#          booksheet2.write(i,j,col)





def SendMail(to_list,subject,content,attfile):
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject,'utf-8')
    msg['From'] = me
    msg['to'] = ",".join(to_list)
#    msg['to'] = to_list
#    to_list = to_list.split(",")
    basename = os.path.basename(attfile)  
    att = MIMEText(open(attfile, 'rb').read(), 'base64', 'gb2312')  
    att_text = MIMEText(content,'html','utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s' % basename.encode('gb2312') 
    msg.attach(att)  
    msg.attach(att_text)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user+'@'+mail_postfix,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        return False


def Cleandir():
  for files in os.listdir(logpath):
    logfile = os.path.join(logpath,files)
    os.remove(logfile)
#    print "remove " + logfile


mail_list = ['huanghuajin@xxx.cn','opt@xxx.cn','raochao@xxx.cn','wangyixuan@xxx.cn']
#mail_list = ['huanghuajin@xxx.cn']

DownloadData()
GenLog()
title = 'xxx页面数据-%s' % day
fname = basepath+'/xxx页面数据_%s.xls' % day
SendMail(mail_list,title,'xxx页面数据,系统自动发送',fname)

Cleandir()

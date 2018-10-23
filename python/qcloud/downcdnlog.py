#!/usr/bin/env python
#coding:utf-8
import sys
import os
#import pandas as pd
import commands
import xlwt
import datetime
import urllib, urllib2
import smtplib
from email.Header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

mail_host ="smtp.exmail.qq.com"
mail_user = ""
mail_postfix = ''
mail_pass = ""


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=22)
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
    cmd = """/usr/bin/python %s/GetDayLog.py xxx.com -u xxx -p xxx --day %s %s""" % (basepath,day,basepath)
    (status,result)=commands.getstatusoutput(cmd)
    if status == 0:
      cmd = """gunzip %s-mini.flash.xxx.com.gz;mv %s-mini.flash.xxx.com %s/%s-xxx.log""" % (day,day,dpath,day)
      (status,result)=commands.getstatusoutput(cmd)
      if status == 0:
        return True
    else:
      print "File download fail."
      return False





def Cleandir():
  for files in os.listdir(logpath):
    logfile = os.path.join(logpath,files)
    os.remove(logfile)
#    print "remove " + logfile


mail_list = ['huanghuajin@xxx.cn']
#mail_list = ['huanghuajin@xxx.cn','opt@xxx.cn']

DownloadData()
#GenLog()
#title = 'xxx页面数据-%s' % day
#fname = basepath+'/xxx页面数据_%s.xls' % day
#SendMail(mail_list,title,'xxx页面数据,系统自动发送',fname)

#Cleandir()

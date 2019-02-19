#coding:utf-8
#cdn刷新
#author：Frank
import sys,os
import urllib
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
from urllib import parse
import requests
 
class Sign:
    def __init__(self,secretId,secretKey):
        self.access_key_id = secretId
        self.access_key_secret = secretKey
 
    def percent_encode(self, encodeStr):
        if isinstance(encodeStr, bytes):
            encodeStr = encodeStr.decode(sys.stdin.encoding)
        res = parse.quote_plus(encodeStr.encode('utf-8'), '')
        res = res.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
        return res
 
    def make(self,requestHost,parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])
        stringToSign = bytes(stringToSign,'utf-8')
        access_key_secret = bytes(self.access_key_secret+"&",'utf-8')
        h = hmac.new(access_key_secret, stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature
 
class Request:
        def __init__(self,secretId, secretKey):
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            self.Format='JSON'
            self.Version='2014-11-11'
            self.AccessKeyId = secretId
            self.secretKey = secretKey
            self.SignatureVersion = '1.0'
            self.SignatureMethod = 'HMAC-SHA1'
            self.SignatureNonce = str(uuid.uuid1())
            self.TimeStamp = timestamp

        def send(self,requestHost,params):
            params["Format"] = self.Format
            params["Version"] = self.Version
            params["AccessKeyId"] = self.AccessKeyId
            params["SignatureVersion"] = self.SignatureVersion
            params["SignatureMethod"] = self.SignatureMethod
            params["SignatureNonce"] = self.SignatureNonce
            params["TimeStamp"] = self.TimeStamp
            sign = Sign(self.AccessKeyId,self.secretKey)
            params["Signature"] = sign.make(requestHost,params)
            url = requestHost
            try:
              req = requests.get(url,params=params)
            except Exception as e:
              print (e)
            return req.text


class Cdn:
    def __init__(self):
      self.secretId = ''
      self.secretKey =''
      self.host = 'http://cdn.aliyuncs.com'
     
    def DescribeUserDomains(self):
      """
      获取cdn加速域名
      """
      params = {
	"Action": 'DescribeUserDomains'
	}
      request = Request(self.secretId,self.secretKey)
      res = request.send(self.host,params)
      return res
    def RefreshObjectCaches(self,url_list,obtype):
      """
      刷新URL或目录
      """
      params = {
	"Action": 'RefreshObjectCaches',
        "ObjectType": obtype,
        "ObjectPath":url_list
	}
      request = Request(self.secretId,self.secretKey)
      res = request.send(self.host,params)
      return res
    def PushObjectCache(self,url_list):
      """
      url预热
      """
      params = {
        "Action": 'RefreshObjectCaches',
        "ObjectPath": url_list
	}
      request = Request(self.secretId,self.secretKey)
      res = request.send(self.host,params)
      return res
    def DescribeRefreshTasks(self,taskId):
      """
	根据taskID查询cdn刷新进度
      """
      params = {
	"Action": 'DescribeRefreshTasks',
        "TaskId": taskId
	}
      request = Request(self.secretId,self.secretKey)
      res = request.send(self.host,params)
      return res

      

# 
if __name__ == '__main__':
    ac = Cdn()
    #params = {'Action': 'RefreshObjectCaches', 'ObjectPath': 'https://www.flash.cn/addialog.php', 'ObjectType': 'File'}
    #res = f.make_request(params)
    #print (res)
    res = ac.DescribeRefreshTasks('4397204535')
    print (res)

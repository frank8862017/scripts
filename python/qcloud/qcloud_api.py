#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import requests
import binascii
import hmac
import random
import sys
import time
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding("utf-8")

try: import simplejson as json
except: import json


class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestHost, requestUri, params, method = 'GET'):
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]


class Request:
    def __init__(self, secretId, secretKey):
        self.timeout = 10
        self.version = 'Python_Tools'
        self.secretId = secretId
        self.secretKey = secretKey

    def send(self, requestHost, requestUri, params, method = 'GET', debug = 0):
        params['RequestClient'] = self.version
        params['SecretId'] = self.secretId
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)
        url = 'https://%s%s' % (requestHost, requestUri)

        if debug:
            print(method.upper(), url)
            print('Request Args:')
            pprint(params)
        if method.upper() == 'GET':
            req = requests.get(url, params=params, timeout=self.timeout, verify=False)
        else:
            req = requests.post(url, data=params, timeout=self.timeout, verify=False)
        if debug:
            print("Response:", req.status_code, req.text)
        if req.status_code != requests.codes.ok:
            return req.status_code
        else:
            return req.text


class Cvm:
    def __init__(self):
        self.secretId = ""
        self.secretKey = ""
        self.host = 'cvm.tencentcloudapi.com'
        self.uri = '/'
        self.method = "GET"
        self.debug = 0


    def DescribeInstances(self):
        """
        查询CVM所有信息
        Action:'DescribeInstances'
        Qcloud API URL: https://cloud.tencent.com/document/api/213/15728
        """
        params = {
            'Nonce': random.randint(1, sys.maxint),
            'Timestamp': int(time.time()),
            'Action': 'DescribeInstances',
            'Version': '2017-03-12',
            'Region': 'ap-shanghai',
            }

        # params["Action"] = 'DescribeCdnHosts'
        request = Request(self.secretId, self.secretKey)
        result = request.send(self.host, self.uri, params, self.method, self.debug)
        result = json.loads(result)
        total_cvm = result["Response"]["TotalCount"]
        print total_cvm
		#分页查询
        Offset,length,i= 0,0,0
        ins= []
        while(i<total_cvm):
          if total_cvm - Offset < 100:
            length = total_cvm - Offset
          else:
            length = 100
          params = {
            'Nonce': random.randint(1, sys.maxint),
            'Timestamp': int(time.time()),
            'Action': 'DescribeInstances',
            'Version': '2017-03-12',
            'Region': 'ap-shanghai',
            'Offset': Offset,
            'Limit': length
            }
          request = Request(self.secretId, self.secretKey)
          result = request.send(self.host, self.uri, params, self.method, self.debug)
          result = json.loads(result)
          instance_lst = result["Response"]["InstanceSet"]
          ins =ins+instance_lst
          i =  i + 100
          Offset = i
        dic={} 
        for line in ins:
          #print line['InstanceName'],line["DataDisks"]
          try:
            disk = line["DataDisks"]
            if disk is not None:
              disklst = []
              for d in disk:
                try:
                  DiskId = str(d["DiskId"])
                  #print DiskId
                  disklst.append(DiskId)
                  #print type(dlst)
                except Exception, e:
                  print e 
              dic[str(line['InstanceName'])] = disklst
          
          #dic["InstanceName"] = line['InstanceName']
          #dic["InstanceId"] = line["InstanceId"]
          #dic["SystemDisk"] = line["SystemDisk"]["DiskId"]
          #dic["DataDisks"] = line["DataDisks"][0]["DiskId"]
          except Exception,e:
            pass
        return  dic



def main():
    action = Cvm()
    project_result = action.DescribeInstances()
    print project_result


if __name__ == '__main__':
    main()

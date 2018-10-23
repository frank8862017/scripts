#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import urllib
import requests
import binascii
import hmac
import copy
import random
import sys
import time
import datetime
import subprocess
import commands
from pprint import pprint
from optparse import OptionParser
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
    timeout = 10
    version = 'Python_Tools'
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def send(self, requestHost, requestUri, params, files = {}, method = 'GET', debug = 0):
        params['RequestClient'] = Request.version
        params['SecretId'] = self.secretId
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)

        url = 'https://%s%s' % (requestHost, requestUri)

        if debug:
            print method.upper(), url
            print 'Request Args:'
            pprint(params)
        if method.upper() == 'GET':
            req = requests.get(url, params=params, timeout=Request.timeout,verify=False)
        else:
            req = requests.post(url, data=params, files=files, timeout=Request.timeout,verify=False)

        if debug:
            print "Response:", req.status_code, req.text
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        rsp = {}
        try:
            rsp = json.loads(req.text)
        except:
            raise ValueError, "Error: response is not json\n%s" % req.text

        code = rsp.get("code", -1)
        message = rsp.get("message", req.text)
        if rsp.get('code', -404) != 0:
            raise ValueError, "Error: code=%s, message=%s" % (code, message)
        if rsp.get('data', None) is None:
            print 'request is success.'
        else:
            return rsp['data']


class Download:
    def __init__(self):
        self.params = {
                'Region': 'gz',
                'Nonce': random.randint(1, sys.maxint),
                'Timestamp': int(time.time()),
                }
        self.files = {}
        self.host = 'cdn.api.qcloud.com'
        self.uri = '/v2/index.php'
        self.method = "POST"
        self.debug = 1
        self.day = ''
        self.secret_id = ''
        self.secret_key = ''
        self.domain = ''

    def download_log(self, host_id):
        del self.params['hosts.0']
        del self.params['Signature']
        del self.params['SecretId']
        self.params['Action'] = 'GenerateLogList'
        self.params['hostId'] = host_id
        self.params['startDate'] = self.day
        self.params['endDate'] = self.day
        request = Request(self.secret_id, self.secret_key)
        data = request.send(self.host, self.uri, self.params, self.files, self.method, self.debug)
        try:
            filename="%s%s-%s"%(self.day,self.hour,self.domain)
            print filename
#            tmp_path = os.path.join(self.dstpath, 'tmp', self.day)
            if not os.path.exists(self.dstpath):
                os.makedirs(self.dstpath)
            for item in data['list']:
                if item.get('link', None) is None:
                    continue
                fname = item['name']
                link = item['link']

                if fname == filename:
                    cmd="wget -q -c -O %s/%s.gz '%s'" % (self.dstpath, fname, link)
                    print cmd
                    subprocess.call(cmd, shell=True)
            file=os.path.join(self.dstpath,filename+".gz")
            print file
            if os.path.exists(file):
                print "file %s is exits,import into hive"
                cmd='source /etc/profile; hive -e \'use cdn ; load data  local inpath "%s" into table cdn_test partition(dt="%s", hour="%s");\''%(file,self.day,self.hour)
                (status, result) = commands.getstatusoutput(cmd)
                if status == 0:
                    os.remove(file)
                    print "import %s file to hive success " %file



        except:
            raise


#            for item in data['list']:
#                if item.get('link', None) is None:
#                    continue
#                fname = item['name']
#                link = item['link']
#                cmd = "wget -q -c -O %s/%s.gz '%s'" % (tmp_path, fname, link)
#                subprocess.call(cmd, shell=True)
#            dst_abs_fname = os.path.join(self.dstpath, '%s-%s.gz' % (self.day, self.domain))
#            if len(os.listdir(tmp_path)) == 0:
#                exit(0)
#            cmd = 'cat %s/* > %s' % (tmp_path, dst_abs_fname)
#            subprocess.call(cmd, shell=True)
#        except:
#            raise

    def parse_args(self):
        usage='usage: %prog host [options] \n\nThis is help message for tools'
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('--debug', dest='debug', action="store_true", default=False, help='Print debug message')
        self.parser.add_option('-u', '--secret_id', dest='secret_id', help='Secret ID from <https://console.qcloud.com/capi>')
        self.parser.add_option('-p', '--secret_key', dest='secret_key', help='Secret Key from <https://console.qcloud.com/capi>')
        self.parser.add_option('--day', dest='day', default="today", help="CDN log day")
        self.parser.add_option('--hour', dest='hour', default="-1", help="CDN log in hour")
        self.parser.add_option('--dstpath', dest='dstpath', default="/app/data/cdn", help="STORE CDN log path")
        from sys import argv
        if len(argv) < 2:
            self.parser.print_help()
            exit(0)
        self.domain = argv[1]
        (options, args) = self.parser.parse_args() # parse again
        for key in dir(options):
            if not key.startswith("__") and getattr(options, key) is None:
                raise KeyError, ('Error: Please provide options --%s' % key)
        self.secret_id = options.secret_id
        self.secret_key = options.secret_key
        self.day = options.day
        self.hour= options.hour
        if self.hour=="-1":
            self.hour= (datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%H")
        else:
            self.hour="%02d" %int(self.hour)

        if self.day == 'today':
            self.day = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y%m%d')
            #self.day = time.strftime('%Y%m%d',  time.localtime()-3600)
        else:
            try:
                format_day = time.strptime(self.day, '%Y%m%d')
            except:
                raise KeyError, ('Error: day format is error, please use YYYY-mm-dd format')
        self.dstpath = options.dstpath
        if self.dstpath == '.':
            self.dstpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.debug = options.debug
        request = Request(self.secret_id, self.secret_key)
        self.params['Action'] = 'GetHostInfoByHost'
        self.params['hosts.0'] = self.domain
        data = request.send(self.host, self.uri, self.params, self.files, self.method, self.debug)
        host_id = 0
        try:
            host_id = data['hosts'][0]['id']
        except:
            raise KeyError, ('Host not invaild')
        self.download_log(host_id)


def main():
    download = Download()
    try:
        download.parse_args()
    except Exception as e:
        print e
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())


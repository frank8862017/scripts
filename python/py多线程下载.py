#coding:utf-8
import requests
import threading

class downloader:
    def __init__(self):
        self.url='https://www.flash.cn/flashplayer/3200142/install_flash_player_cn.exe'
        self.num=8
        self.name=self.url.split('/')[-1]
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        print 'total is %s' % (self.total)
    def get_range(self):
        ranges=[]
        offset = int(self.total/self.num)
        for i in  range(self.num):
            if i==self.num-1:
                ranges.append((i*offset,''))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges
    def download(self,start,end):
        headers={'Range':'Bytes=%s-%s' % (start,end),'Accept-Encoding':'*'}
        res = requests.get(self.url,headers=headers)
        print '%s:%s download success'%(start,end)
        self.fd.seek(start)
        self.fd.write(res.content)
    def run(self):
        self.fd =  open(self.name,'w')
        thread_list = []
        n = 0
        for ran in self.get_range():
            start,end = ran
            print 'thread %d start:%s,end:%s'%(n,start,end)
            n+=1
            thread = threading.Thread(target=self.download,args=(start,end))
            thread.start()
            thread_list.append(thread)
        for i in thread_list:
            i.join()
        print 'download %s load success'%(self.name)
        self.fd.close()
if __name__=='__main__':
    down = downloader()
    down.run()

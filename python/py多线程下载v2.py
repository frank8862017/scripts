import requests
from multiprocessing.dummy import Pool


class Downloader():
    __slots__ = ['url', 'name', 'length', 'offset', 'pool']

    url = None
    name = None
    length = None
    offset = None
    pool = None

    def __init__(self, url):
        self.url = url
        self.get_pool()
        self.get_name()
        self.get_length()
        self.get_offset()
    
    def get_pool(self, processes=None):
        '''
        获取多线程池，不指定线程数时，使用系统默认值
        不建议指定线程数量，在不同的机器上，过多或过少的线程，反而会因为管理线程耗费额外的开销
        可以尝试指定不同的线程数，对比处理速度
        '''

        if processes and type(processes) is int:
            self.pool = Pool(processes)
        else:
            self.pool = Pool()

    def get_name(self):
        '''
        获取保存文件名
        '''

        self.name = url.split('/')[-1]

    def get_length(self):
        '''
        获取下载文件长度
        '''

        response = requests.head(self.url)
        if response.ok:
            self.length = int(response.headers.get('content-length', 0))
        else:
            self.length = None

    def get_offset(self):
        '''
        计算分块下载长度
        注意 python 中运算符「/」，如果两边的数都是整数，计算的结果也是整数
        '''
        if self.length and self.pool:
            self.offset = self.length / self.pool._processes

    def get_ranges(self):
        '''
        计算分块下载时，各分块的起始位置
        '''

        if self.offset:
            ranges = range(0, self.length, self.offset)
            ranges = [(start, start + self.offset) for start in ranges]
            return ranges
        else:
            return []

    def _save(self, data):
        '''
        使用 seek 将分块下载到的数据写到文件中指定的位置
        '''

        with open(self.name, 'w') as _file:
            for _data in data:
                _file.seek(_data[0][0])
                _file.write(_data[1])

    def _download(self, _range):
        '''
        单线程下载指定区块数据
        '''

        headers = {'Range': 'Bytes=%d-%d' % _range}
        response  = requests.get(self.url, headers=headers)
        if response.ok:
            return (_range, response.content)
        else:
            return (_range, '')

    def download(self):
        '''
        分块下载数据，注意这里的 Pool.map 用法
        '''
        ranges = self.get_ranges()
        if ranges:
            result = self.pool.map(self._download, ranges)
            self._save(result)

if __name__ == '__main__':
    url = 'http://51reboot.com/src/blogimg/pc.jpg'
    downloader = Downloader(url)
    downloader.download()
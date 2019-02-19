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
        ��ȡ���̳߳أ���ָ���߳���ʱ��ʹ��ϵͳĬ��ֵ
        ������ָ���߳��������ڲ�ͬ�Ļ����ϣ��������ٵ��̣߳���������Ϊ�����̺߳ķѶ���Ŀ���
        ���Գ���ָ����ͬ���߳������Աȴ����ٶ�
        '''

        if processes and type(processes) is int:
            self.pool = Pool(processes)
        else:
            self.pool = Pool()

    def get_name(self):
        '''
        ��ȡ�����ļ���
        '''

        self.name = url.split('/')[-1]

    def get_length(self):
        '''
        ��ȡ�����ļ�����
        '''

        response = requests.head(self.url)
        if response.ok:
            self.length = int(response.headers.get('content-length', 0))
        else:
            self.length = None

    def get_offset(self):
        '''
        ����ֿ����س���
        ע�� python ���������/����������ߵ�����������������Ľ��Ҳ������
        '''
        if self.length and self.pool:
            self.offset = self.length / self.pool._processes

    def get_ranges(self):
        '''
        ����ֿ�����ʱ�����ֿ����ʼλ��
        '''

        if self.offset:
            ranges = range(0, self.length, self.offset)
            ranges = [(start, start + self.offset) for start in ranges]
            return ranges
        else:
            return []

    def _save(self, data):
        '''
        ʹ�� seek ���ֿ����ص�������д���ļ���ָ����λ��
        '''

        with open(self.name, 'w') as _file:
            for _data in data:
                _file.seek(_data[0][0])
                _file.write(_data[1])

    def _download(self, _range):
        '''
        ���߳�����ָ����������
        '''

        headers = {'Range': 'Bytes=%d-%d' % _range}
        response  = requests.get(self.url, headers=headers)
        if response.ok:
            return (_range, response.content)
        else:
            return (_range, '')

    def download(self):
        '''
        �ֿ��������ݣ�ע������� Pool.map �÷�
        '''
        ranges = self.get_ranges()
        if ranges:
            result = self.pool.map(self._download, ranges)
            self._save(result)

if __name__ == '__main__':
    url = 'http://51reboot.com/src/blogimg/pc.jpg'
    downloader = Downloader(url)
    downloader.download()
# coding=utf-8
#https://github.com/shengxinjing
import sys
import time

class Tail():
    def __init__(self,file_name,callback=sys.stdout.write):
        self.file_name = file_name
        self.callback = callback
    def follow(self,n=10):
        try:
            # ���ļ�
            with open(self.file_name) as f:
                self._file = f
                self._file.seek(0,2)
                # �洢�ļ����ַ�����
                self.file_length = self._file.tell()
                # ��ӡ���10��
                self.showLastLine(n)
                # �������ļ� ��ӡ����
                while True:
                    line = self._file.readline()
                    if line:
                        self.callback(line)
                    time.sleep(1)
        except Exception,e:
            print '���ļ�ʧ�ܣ��壬�����ļ��ǲ��ǲ����ڣ�����Ȩ��������'
            print e
    def showLastLine(self, n):
        # һ�д��100���� ������ĳ�1����1000����
        len_line = 100
        # nĬ����10��Ҳ����follow�Ĳ���������
        read_len = len_line*n
        # ��last_lines�洢���Ҫ���������
        while True:
            # ���Ҫ��ȡ��1000���ַ�������֮ǰ�洢���ļ�����
            # �����ļ���ֱ��break
            if read_len>self.file_length:
                self._file.seek(0)
                last_lines = self._file.read().split('\n')[-n:]
                break
            # �ȶ�1000�� Ȼ���ж�1000���ַ��ﻻ�з�������
            self._file.seek(-read_len, 2)
            last_words = self._file.read(read_len)
            # count�ǻ��з�������
            count = last_words.count('\n')

            if count>=n:
                # ���з���������10 �ܺô���ֱ�Ӷ�ȡ
                last_lines = last_words.split('\n')[-n:]
                break
            # ���з�����10��
            else:
                # break
                #����ʮ��
                # ���һ�����з�Ҳû�У���ô���Ǿ���Ϊһ�д����100��
                if count==0:

                    len_perline = read_len
                # �����4�����з���������Ϊÿ�д����250���ַ�
                else:
                    len_perline = read_len/count
                # Ҫ��ȡ�ĳ��ȱ�Ϊ2500�����������ж�
                read_len = len_perline * n
        for line in last_lines:
            self.callback(line+'\n')
if __name__ == '__main__':
    py_tail = Tail('test.txt')
    py_tail.follow(20)
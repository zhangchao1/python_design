#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2015-12-28

class base_file:

    '''
    构造函数传入文件路径，以及文件读取模式
    'r' :写入模式
    'w' :写入模式
    '''
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode
        self.file = open(path, mode)

    '''
    写入文件
    '''
    def write_data_to_file(self, content):
        self.file.write("%s\n", content)

    '''
    读取文件
    '''
    def read_data_from_file(self):
        return self.file

    '''
    构析函数关闭文件
    '''
    def __del__(self):
        self.file.close()

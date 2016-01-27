#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2015-12-28

from multiprocessing import Pool

class process_pool:

    '''
    初始化进程池
    '''
    def __init__(self, sum_process ,initializer=None, initargs=(), maxtasksperchild=None):
        self.sum_process = sum_process
        self.pool = Pool(self.sum_process,initializer,initargs,maxtasksperchild)

    '''
    关闭所有的进程
    '''
    def __del__(self):
        self.pool.close()
        self.pool.join()

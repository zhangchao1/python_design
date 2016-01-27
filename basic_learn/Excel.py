#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2015-12-29

import xlrd as er
import xlwt as ew

class Excel:
    '''
    将excel的一些操作封装起来，然后封装一些初始化的操作
    将excel的读取和写入放在同一个类中
    mode = r 读取excel文档
    mode = w 写入excel文档
    '''
    def __init__(self, path, mode):
        self.mode = mode
        if  self.mode == 'r':
            self.excel = er.open_workbook(path)
        if  self.mode == 'w':
            self.excel = ew.Workbook()

#########集中写的是excel关于写入的操作##########
####### 不要混用这个方法########################
    '''
    初始化excel表格写入
    '''
    def add_sheet_name(self, name):
        if self.mode == 'w':
            return self.excel.add_sheet(name)
        else:
            print "your operation is wrong"

    '''
    初始化excel的表格对应的表名
    '''
    def add_cow_name(self, line, cow, data,sheetobject):
        if self.mode == 'w':
            sheetobject.write(line, cow, u"%s"%data)
        else:
            print "your operation is wrong"
    '''
    保存新的excel
    '''
    def save(self, name):
        if self.mode == 'w':
            self.excel.save(name)
        else:
            print "your operation is wrong"
##########集中处理的是excel关于读取的方法进行####
#########这里的方法不要混用##############
    '''
    根据sheet页名字获取打开文件
    '''
    def get_sheet_name(self, name):
        if self.mode == 'r':
            return self.excel.sheets()[name]
        else:
            return  False

    '''
    获取当前sheet页的最大行数和列数
    '''
    def get_max_lineCoW(self, sheetObject):
        return sheetObject.nrows , sheetObject.ncols

    '''
    根据参数来获取对应行数和列数的数值
    type = 'c' 读取列
    type = 'r' 读取行
    '''
    def get_data_from_sheet(self,sheetObject, type, count):
        if type == 'r':
            return sheetObject.row_values(count)
        if type == 'c':
            return sheetObject.col_values(count)

    '''
    根据坐标形式获取对应的内容
    '''
    def get_data_by_coordinate(self, sheetObject, row, column):
        return sheetObject.cell_value(row,column)
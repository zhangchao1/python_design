#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2015-12-12

import os
class base_log:
    '''
    函数：格式化时间
    参数：输入的时间
    作用：格式化时间为20151212，满足log文件名判断
    '''
    def format_time(self, input_time, filter_style="-"):
        if filter_style == "-":
            input_time = str(input_time)
            return input_time.replace(filter_style,"")

    '''
    函数：路径存在
    参数：路径
    作用：判断路径是否存在
    '''
    def path_exist(self,file_path):
        return os.path.exists(file_path)

    '''
    函数：获取路径的文件
    参数：路径
    作用：获取路径下的所有文件
    '''
    def get_all_file(self, file_path, filter_style=""):
        if filter_style == "":
            return os.listdir(file_path)

    '''
    函数：拼接路径
    参数：路径，文件
    作用：返回拼接好的路径 保证在每个系统下的运行
    '''
    def split_join_path(self, path, file):
        return os.path.join(path ,file)

    '''
    函数：存入文件内容
    参数：文件名
    作用：将单个log的文件内容存入字典当中
    '''
    def store_file_contents_to_dicitionaries(self, path, file_name, seg_rule, list_len, key_list=[], file_dic={}):
        #####初始化的一个字典，存储单个的文件内容########
        filepath = self.split_join_path(path, file_name)
        file_obj = open(filepath,'r')
        for i in file_obj:
            i = i.replace("\n","")
            line_data = i.split(seg_rule,list_len)
            for c in range(0,len(key_list)):
                key = key_list[c]
                file_dic[key].append(line_data[c])
        file_obj.close()
        return file_dic

    '''
    函数：合并字典
    参数：传入两个字典
    作用：合并log文件
    '''
    def merger_two_dic(self, dic1, dic2):
        if dic1:
            for i in dic1:
                if dic2.has_key(i):
                    for m in range(0,len(dic2[i])):
                        dic1[i].append(dic2[i][m])
            return dic1
        else:
            return dic2

    '''
    函数：获取传入时间对应文件下的所有文件
    参数：路径，时间参数
    作用：获取文件下的所有文件
    '''
    def get_all_log_file(self, path, time):
        time = self.format_time(time)
        log_file_path = self.split_join_path(path,time)
        if self.path_exist(log_file_path):
            all_file =  self.get_all_file(log_file_path)
            return all_file ,log_file_path ,len(all_file)
        else:
            return None

    '''
    获取目录下的所有文件，使用os.walk方法进行获取
    '''
    def get_all_dir_file(self,path):
        all_file_obj = os.walk(path)
        all_file = []
        for path ,dir ,filelist in all_file_obj:
            for filename in filelist:
                all_file.append(os.path.join(path,filename))
        return all_file



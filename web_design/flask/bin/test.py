#coding:utf-8
#
# import os, sys
# parentdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src");
# if parentdir not in sys.path:
#     sys.path.insert(0, parentdir);
#
# import omen.service.IPAnalysiseService

def test():
    for i in range(0,50):
        yield i
data = test()
for i in data:
    print i
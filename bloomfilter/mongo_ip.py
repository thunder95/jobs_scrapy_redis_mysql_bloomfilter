#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import random

conn = pymongo.MongoClient('localhost', 27017)
db = conn.proxy
tb = db.proxys
#total = tb.count()
total = tb.count({'protocol':{'$gt':0}})

def GetIP():


    #从mongo中随机取出一条
    num = random.randint(1, total-1)
    #rs = tb.find().limit(1).skip(num).sort([("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
    rs = tb.find({'protocol':{'$gt':0}}).limit(1).skip(num).sort([("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])

    data = list(rs)[0]
    proxy_ip = "http://{0}:{1}".format(data['ip'], data['port'])
    print("proxy_ip: "+proxy_ip)
    return proxy_ip
    #return {'http': proxy_ip, 'https': proxy_ip}
   
if __name__ == "__main__":
    print(GetIP())

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#scrapy redis pipeline
#class ProxyTestPipeline(object):
    #def process_item(self, item, spider):
        #return item


from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import sys

reload(sys)  
sys.setdefaultencoding('utf8')


class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbpool=adbapi.ConnectionPool("pymysql",host=settings["MYSQL_HOST"],port=settings["MYSQL_PORT"], db=settings["MYSQL_DBNAME"],user=settings["MYSQL_USER"],password=settings["MYSQL_PASSWORD"],charset="utf8", cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        
        self.dbpool.runInteraction(self.do_insert,item)


    def do_insert(self,cursor,item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中

        #if not item.has_key('otherq'):
            #item['otherq'] = ''
        #if not item.has_key('spider_name'):
            #item['spider_name'] = 'unknown'
        #print 'spider_name===================>', item['spider_name']

        # 使用execute方法执行SQL INSERT语句
        sql = '''insert into job values(null,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")on duplicate key update ''' \
              '''area=values(area),salary=values(salary),exp=values(exp),edu=values(edu),num=values(num),time=values(time),otherq=values(otherq),welfare=values(welfare)''' \
              ''',info=values(info),local=values(local),co_url=values(co_url),co_type=values(co_type)''' % \
              (item['name'], item['co_name'], item['area'], item['salary'],item['exp'],item['edu'], item['num'], item['time'],
               item['otherq'],item['welfare'],item['info'], item['local'], item['co_url'], item['co_type'],item['spider_name'], item['target_id'])

        cursor.execute(sql)

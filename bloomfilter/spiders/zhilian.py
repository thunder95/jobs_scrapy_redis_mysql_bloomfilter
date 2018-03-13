# -*- coding: utf-8 -*-
import scrapy
import time,re
import hashlib
from bloomfilter.items import ZhilianItem
from redis_bloom.spiders import RedisSpider
from bloomfilter.utils import get_num, getVal, crate_params, MORE_PAGE, get_qs, md5
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

# 导入redis包

#class ZhilianSpider(scrapy.Spider):
class ZhilianSpider(RedisSpider):
    name = 'zhilian'
    #redis_key = 'zhilian:start_urls'
    allowed_domains = ['zhaopin.com']
    rule_key = "http://zhaopin.com/"
   
    # 分布式爬虫 使用parse
    def parse(self,response):
        # start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx"
        # 起始请求获取相应检索条件
        start_url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20171221"
        yield scrapy.Request(url=start_url,callback=self.parse_start, dont_filter=True)

    '''
    http://sou.zhaopin.com/jobs/searchresult.ashx?jl=城市&isadv=0&ct=公司性质&isfilter=1&p=1&et=职位类型&el=学历
    页数：p
    职位类型et：不限：et=-1
                全职：et=2
                兼职：et=1
                实习：et=4
                校园：et=5
    公司性质：ct ：-1 到 16
    学历：el   ：-1，-2，1，3,4,5,7,8
    '''
    # 解析城市等信息接口，组装完整的搜索url
    def parse_start(self, response):
        # 获取城市
        # print response.body
        info = response.body

        # 第一次 获取 var dCity 后面的城市信息 ID+城市
        pattern = re.compile(r"var dCity = '(.*?)0@';")
        city_info = pattern.findall(info)
        citys = []
        if len(city_info)>0 :
            city_info2 = city_info[0].decode("utf-8")
            # 第二次获取中文字段的城市(unicode格式)
            chn = re.compile(ur'[\u4e00-\u9fa5]+')
            city_list = chn.findall(city_info2)
            for city in city_list:
                city = city.encode("utf-8")
                citys.append(city)

        # 排除掉的省
        sheng= ['全国','广东','湖北','陕西','四川','辽宁','吉林','江苏','山东','浙江','广西','安徽','河北','山西','内蒙','黑龙江','福建','江西','河南','湖南','海南','贵州','云南','西藏','甘肃','青海','宁夏','新疆']
        s = set(sheng)
        citys = set(citys)
        # 存 放城市 ,对称差集更新操作
        citys.symmetric_difference_update(s)
        # 最终获取筛选出来的城市
        city_list = list(citys)
        # print city_list
        # 公司性质
        companyNO_ct = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        # 学历
        educationNO_el = [-1,1,3,4,5,7,8]
        # 职位类型
        positioinNO_et = [1,2,4,5]
        #base_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&isadv=0&ct=%s&isfilter=1&et=%s&el=%s"
        #city_list = ['成都']
        for city in city_list:
            for ct in companyNO_ct:
                for et in positioinNO_et:
                    for el in educationNO_el:
                        # # 翻页
                        # for page in range(1,91):
                            #print city+"  下面的:"+"公司类型"+str(ct)+"学历"+str(el)+"职位类型"+str(et)
                            #full_url = base_url % (city,str(ct),str(page),str(et),str(el))
                        #full_url = base_url % (city,str(ct),str(et),str(el))
                        #yield scrapy.Request(full_url, callback=self.parse_list, headers=self.headers, priority=1)
                        full_url = self.rule_key +crate_params('0', (city,str(ct),str(et),str(el), '1'))
                        yield scrapy.Request(url=full_url,callback=self.parse_list, dont_filter=True,priority=2)

    # 解析列表
    def parse_list(self,response):

        # 获取当前招聘详情的url列表
        recruit_url = response.xpath('//div[@class="newlist_list_content"]//td[@class="zwmc"]//a/@href').extract()
        for url in recruit_url:
            # 筛选排除校园招聘 的url
            if 'jobs.zhaopin.com' in url:
                # print '详情招聘页链接:',url
                # 请求详情页信息
                posi = self.rule_key + crate_params('1', (get_num(url),))
                #yield scrapy.Request(url,callback=self.parse_detail,priority=2)
                yield scrapy.Request(posi,callback=self.parse_detail,priority=3)

        # 获取下一页是否存在url
        next_page = response.xpath('//div[@class="pagesDown"]//li/a[@class="next-page"]/@href').extract()
        # 有下一页分页，再次请求当前parse_list方法请求，再次解析（递归，知道 没有下一页为止）
        print 'nex page==============>',next_page
        if next_page and MORE_PAGE:
            qs = get_qs(str(next_page[0]))
            city = unicode(qs['jl'], "utf-8")
            ct = qs['ct']
            et = qs['et']
            el = qs['el']
            p = qs['p']

            full_url = self.rule_key +crate_params('0', (city,str(ct),str(et),str(el), str(p)))
            yield scrapy.Request(url=full_url,callback=self.parse_list,priority=1)

    # 详情页解析
    def parse_detail(self,response):

        item = ZhilianItem()
        #html = response.body.decode('utf-8')
        #print html
        name = response.xpath('//div[@class="bread_crumbs"]//a[3]/strong/text()')[0].extract().encode('utf-8')
        # 公司福利
        welfare_list = response.xpath('//div[@class="fixed-inner-box"]//span/text()').extract()
        welfare = " ".join(welfare_list).encode("utf-8")

        left_info = response.xpath('//div[@class="terminalpage-left"]')
        for i in left_info:
            salary = i.xpath('.//ul/li[1]/strong/text()')[0].extract().encode('utf-8') # 薪资

            area_city = i.xpath('./ul/li[2]/strong/a/text()').extract()[0].encode('utf-8') # 工作区域_市
            area_qu = i.xpath('./ul/li[2]/strong/text()').extract() # 工作区域_区
            area_qu = getVal(area_qu)
            if area_qu !="":
                area_qu = area_qu[0].encode("utf-8")
            area = area_city+area_qu   # 完整的工作区域

            exp = i.xpath('.//ul/li[5]/strong/text()')[0].extract().encode('utf-8') # 经验
            edu = i.xpath('.//ul/li[6]/strong/text()')[0].extract().encode('utf-8') # 学历
            num = i.xpath('.//ul/li[7]/strong/text()')[0].extract().encode('utf-8') # 人数
            time = i.xpath('.//ul/li[3]/strong/span/text()')[0].extract().encode('utf-8') # 发布日期：

        local = response.xpath('//div[@class="tab-inner-cont"]//h2/text()')[0].extract().encode('utf-8') # 工作地点 去换行
        local = local.replace('\n','').strip()

        info = response.xpath('//div[@class="tab-inner-cont"]//p/text()').extract()
        # info = '\n'.join(info).encode('utf-8').replace('\n','').strip()  #转了utf-8
        info = '\n'.join(info).replace('\n','').strip()
        #print info
        co_name = response.xpath('//div[@class="terminalpage-right"]//p[@class="company-name-t"]//a/text()')[0].extract().encode('utf-8') # 公司名称
        co_type = response.xpath('//div[@class="terminalpage-right"]//ul/li[2]/strong/text()')[0].extract().encode('utf-8') # 公司类别(公司性质)
        '''
        li_count = response.xpath('//div[@class="terminalpage-right"]//ul/li')[0].extract()
        # co_url = response.xpath('//div[@class="terminalpage-right"]//div[@class="company-box"]//ul/li[4]/strong/a/@href').extract()[0]
        # 有五个li，有网址
        co_url = ""
        i = len(li_count)
        if i == 5:
            # print response.body.decode('utf-8')
            # 公司链接 href为空
            co_url = response.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/a/text()')[0].extract()
        else:
            co_url = "该公司没有网站"
        '''
        co_url = response.xpath('//div[@class="terminalpage-right"]//p[@class="company-name-t"]//a/@href')[0].extract().encode('utf-8') # 该公司在智联上的介绍url
        # print co_url
        # 封装item
        item['name'] = name
        item['welfare'] = welfare
        item['salary'] = salary
        item['area'] = area
        item['exp'] = exp
        item['edu'] = edu
        item['num'] = num
        item['time'] = time
        item['local'] = local
        item['info'] = info
        item['co_name'] = co_name
        item['co_type'] = co_type
        item['co_url'] = co_url
        #添加spider_name
        item['spider_name'] = 'zhilian'
        item['otherq'] = ''
        #识别id
        try:
            item['target_id'] = get_num(response.xpath("//link[@rel='alternate']/@href").extract()[0])
        except:
            item['target_id'] = ''
        return item
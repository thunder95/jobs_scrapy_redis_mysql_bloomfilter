# -*- coding: utf-8 -*-
import scrapy
from bloomfilter.items import Job51Item
from redis_bloom.spiders import RedisSpider
from bloomfilter.utils import get_num, getVal, crate_params, MORE_PAGE, get_qs

class FiveoneSpider(RedisSpider):
    name = 'fiveone'
    allowed_domains = ['51job.com']
    #redis_key = 'job51:start_url'
    rule_key = "http://51job.com/"

    # 获取城市列表
    city_list = ['102000', '091800', '120400', '071300', '200600', '241100', '240800', '161300', '201200', '070800', '100400', '032800', '210800', '220300', '310500', '090700', '180300', '131000', '081400', '190800', '290200', '130700', '230500', '191300', '200800', '140600', '320900', '250400', '190600', '032900', '210300', '121600', '031700', '110500', '071400', '191400', '160900', '270900', '251300', '031800', '071000', '170200', '030700', '290400', '081100', '170800', '030500', '190300', '171400', '091400', '120700', '090800', '260300', '100700', '120600', '120500', '200700', '080400', '100500', '251400', '281000', '281200', '310200', '070400', '150300', '140700', '290300', '180200', '270700', '311000', '101000', '200200', '091900', '320200', '251500', '281400', '110300', '181400', '181300', '200300', '180500', '190400', '191500', '180900', '170700', '130600', '211100', '171200', '281300', '161100', '071100', '171100', '151400', '171800', '110700', '101500', '100300', '300500', '030400', '032400', '201100', '171300', '020000', '131200', '031400', '191000', '080500', '040000', '181700', '230200', '180600', '310800', '160200', '290500', '221100', '210900', '240600', '240700', '070300', '072000', '151600', '181200', '220400', '091500', '311500', '080800', '121100', '072300', '071800', '071600', '210200', '160500', '050000', '181600', '270600', '231200', '240500', '280700', '200500', '150800', '260600', '311100', '311400', '101200', '091000', '231300', '130500', '171000', '271000', '110600', '251100', '171600', '221300', '220600', '260900', '261000', '260800', '181500', '140900', '160600', '120300', '031900', '271300', '100600', '101600', '250300', '110400', '081200', '300300', '121200', '300200', '121800', '141300', '270200', '160300', '090400', '250600', '081000', '071200', '092300', '121700', '231100', '240400', '300400', '251800', '210500', '101400', '271400', '120800', '102100', '140400', '151200', '260400', '111000', '271200', '191200', '211200', '170300', '090500', '171500', '150500', '032300', '032600', '091200', '090300', '220700', '300700', '130200', '091100', '070200', '140200', '110800', '070900', '170600', '090900', '080300', '110900', '251900', '220900', '130900', '240300', '120200', '120900', '171900', '080700', '270400', '220800', '031500', '170500', '032200', '270300', '080600', '230700', '210700', '211000', '180800', '180700', '130400', '072500', '130300', '270500', '310400', '170400', '032700', '310300', '311700', '250200', '070600', '220200', '310700', '320500', '320300', '100200', '320700', '081600', '320400', '160700', '200900', '080200', '121400', '311600', '150200', '141200', '032100', '171700', '221000', '141500', '221200', '161200', '190500', '251000', '280200', '281100', '230900', '080900', '191100', '071900', '151700', '151100', '181100', '320600', '151000', '180400', '030300', '091700', '250500', '230300', '220500', '210400', '221400', '230800', '072100', '251600', '090600', '121300', '172000', '252000', '101100', '271100', '100900', '121000', '030800', '100800', '280800', '181000', '181800', '140800', '030600', '110200', '230600', '131100', '231500', '150700', '271500', '092100', '130800', '290600', '091300', '091600', '030200', '140300', '141000', '260200', '320800', '092200', '310600', '310900', '281500', '311300', '300800', '230400', '201000', '150400', '260500', '170900', '280900', '311800', '092000', '241000', '101800', '240900', '270800', '141100', '150600', '280400', '160400', '251200', '101700', '200400', '140500', '010000', '231000', '260700', '121500', '311900', '151800', '160800', '300600', '311200', '101900', '190700', '070700', '070500', '240200', '190200', '210600', '231400', '032000', '190900', '090200', '101300', '161000', '151500', '280300', '141400', '150900', '251700', '060000']

    #city_list = ['090200']
    # 获取工资列表
    salary_list = ['01','02','03','04','05','06','07','08','09','10','11','12']

    #学历列表
    edu_list = ['01','02','03','04','05','06']

    #学历类别
    edu_type = ['初中及以下'.decode('utf8'),'高中'.decode('utf8'),'中技'.decode('utf8'),'中专'.decode('utf8'),'大专'.decode('utf8'),'本科'.decode('utf8'),'硕士'.decode('utf8'),'博士'.decode('utf8')]


    #职位信息中不需要的信息
    unrequire = ['分享'.decode('utf8'),'微信'.decode('utf8'),'邮件'.decode('utf8')]


    #基于不同的城市,工资,学历的第一页请求
    def parse(self, response):
        for cityid in self.city_list:
            for salaryid in self.salary_list:
                for eduid in self.edu_list:
                    #fullurl = self.base_urls % (cityid,salaryid,'%2B',eduid,'%2C')
                    #yield scrapy.Request(url=fullurl,callback=self.page1_parse)

                    full_url = self.rule_key + crate_params('0', (cityid,salaryid,'%2B', '1',eduid,'%2C'))
                    yield scrapy.Request(url=full_url,callback=self.page1_parse, dont_filter=True, priority=2)

                    

    #提取职位url,如果页码大于1,生成所有页码的请求加入队列
    def page1_parse(self, response):
        position = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        if position is not None:
            for posi in position:
                posi_url = posi.xpath('./p//a/@href').extract()[0]
                print '===========>', posi_url
                posi_url = self.rule_key + crate_params('1', (self.get_job(posi_url),))
                yield scrapy.Request(url=posi_url,callback=self.detail_parse,priority=3)

            page = int(response.xpath('//div[@class="rt"][2]/text()').extract()[1].split('/')[1].strip())
            if page != 1 and MORE_PAGE:
                for p in range(2,page+1):
                    #next_url = response.url.replace('1.html', str(p) + '.html')
                    #yield scrapy.Request(url=next_url,callback=self.pages_parse)
                    qs = get_qs(response.url)
                    eduid = qs['degreefrom']
                    cityid = get_num(response.url.split(',')[0])
                    salaryid = response.url.split(',')[5]
                    full_url = self.rule_key + crate_params('0', (cityid,salaryid,'%2B', str(p),eduid,'%2C'))
                    yield scrapy.Request(url=full_url,callback=self.pages_parse,priority=1)

    #页码大于1的页面处理函数
    def pages_parse(self,response):
        position = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for posi in position:
            posi_url = posi.xpath('./p//a/@href').extract()[0]
            #yield scrapy.Request(url=posi_url,callback=self.detail_parse,priority=1)
            posi_url = self.rule_key + crate_params('1', (self.get_job(posi_url),))
            yield scrapy.Request(url=posi_url,callback=self.detail_parse,priority=3)

    #职位详情页
    def detail_parse(self,response):
        #判断信息是否存在
        ifexists = lambda x: x[0] if x else ''
        job = Job51Item()
        #职位名称
        job['name'] = response.xpath('//div[@class="tHeader tHjob"]//h1//text()').extract()[0]
        #公司名称
        job['co_name'] = response.xpath('//p[@class="cname"]/a//text()').extract()[0]
        #区域
        job['area'] = response.xpath('//div[@class="tHeader tHjob"]//span/text()').extract()[0]
        #工资
        job['salary'] = ifexists(response.xpath('//div[@class="tHeader tHjob"]//strong/text()').extract())
        #所有要求
        #其他要求
        otherq = ''
        all_require = response.xpath('//div[@class="tBorderTop_box bt"]//div[@class="t1"]/span/text()').extract()
        for require in all_require:
            if '经验'.decode('utf8') in require:
                job['exp'] = require
            elif require in self.edu_type:
                job['edu'] = require
            elif '人'.decode('utf8') in require:
                job['num'] = require
            elif '发布'.decode('utf8') in require:
                job['time'] = require
            else:
                otherq = otherq + require + ' '
        job['otherq'] = otherq
        #福利
        welfare = ' '
        fuli = response.xpath('//div[@class="tBorderTop_box bt"]//p[@class="t2"]/span/text()').extract()
        for f in fuli:
            welfare = welfare + f + ' '
        job['welfare'] = welfare
        #职位信息
        posi_info = response.xpath('//div[@class="tBorderTop_box"][1]//div[@class="bmsg job_msg inbox"]//text()').extract()
        for i in posi_info:
            if i in self.unrequire:
                posi_info.remove(i)
            else:
                i.strip()
        job['info'] = ' '.join(posi_info)
        #上班地址
        job['local'] = ifexists(response.xpath('//div[@class="tBorderTop_box"]/div[@class="bmsg inbox"]//p/text()[2]').extract())
        #公司网址
        job['co_url'] = response.xpath('//div[@class="tHeader tHjob"]//p[@class="cname"]/a/@href').extract()[0]
        #公司类型
        str1 = response.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()').extract()[0]
        strtotal = ''
        strlist = str1.split('|')
        for s in strlist:
            strtotal = strtotal + s.strip() + '|'
        job['co_type'] = strtotal
        job['spider_name'] = 'job51'
        #识别id
        try:
            job['target_id'] = get_num(response.url.replace('51job', ''))
        except:
            job['target_id'] = ''

        yield job



   

    #获取详情url
    def get_job(self, string):
        return string.split('.html')[0].replace('http://jobs.51job.com/', '')
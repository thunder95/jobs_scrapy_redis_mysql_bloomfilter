# -*- coding: utf-8 -*-
import scrapy
#from liepin.industries import industries
#from liepin.city import city
from bloomfilter.items import LiepinItem
from redis_bloom.spiders import RedisSpider
from bloomfilter.utils import get_num, crate_params, MORE_PAGE, get_qs


class LiePinSpider(RedisSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    #redis_key = 'liepin:start_url'
    rule_key = "http://www.liepin.com/"

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.2,
        "CONCURRENT_REQUESTS": 16
    }
    

    #行业类别列表
    #indusList = ['040']
    indusList = ['040', '420', '010', '030', '050', '060', '020', '080', '100', '090', '130', '140', '150', '430', '500', '190', '240', '200', '210', '220', '460', '470', '350', '360', '180', '370', '340', '270', '280', '290', '330', '310', '320', '300', '490', '120', '110', '440', '450', '230', '260', '510', '070', '170', '380', '250', '160', '480', '390', '410', '400']

    #城市类别列表
    cityList = ['010', '020', '030', '040', '050020', '050030', '050040', '050050', '050060', '050070', '050080', '050090', '050100', '050110', '050120', '050130', '050140', '050150', '050160', '050170', '050180', '050190', '050200', '050210', '050220', '050230', '050240', '050250', '050260', '050270', '050280', '050290', '060020', '060030', '060040', '060050', '060060', '060070', '060080', '060090', '060100', '060110', '060120', '060130', '060140', '060150', '060160', '060170', '060190', '060200', '060210', '060220', '060230', '060240', '060250', '060260', '060270', '060280', '060290', '060300', '060310', '060320', '070020', '070030', '070040', '070050', '070060', '070070', '070080', '070090', '070100', '070110', '070120', '070130', '070140', '070150', '070160', '070170', '070180', '070190', '070200', '070210', '070220', '070230', '070240', '070250', '070260', '070270', '070280', '070290', '070300', '070310', '070320', '070330', '070340', '080020', '080030', '080040', '080050', '080060', '080070', '080080', '080090', '080100', '080110', '080120', '080130', '080140', '080150', '080160', '080170', '080180', '080190', '080200', '080210', '090020', '090030', '090040', '090050', '090060', '090070', '090080', '090090', '090100', '090110', '090120', '090130', '100020', '100030', '100040', '100050', '100060', '100070', '100080', '100090', '100100', '100110', '100120', '100130', '100140', '100150', '110020', '110030', '110040', '110050', '110060', '110070', '110080', '110090', '110100', '110110', '110120', '110130', '110140', '110150', '120020', '120030', '120040', '120050', '120060', '120070', '120080', '120090', '120100', '130020', '130030', '130040', '130060', '130070', '130080', '130090', '130100', '130110', '130120', '130130', '130140', '130150', '130160', '130170', '130180', '130190', '130200', '130210', '140020', '140030', '140040', '140050', '140060', '140070', '140080', '140090', '140100', '140110', '140120', '140130', '140140', '140150', '140160', '140170', '150020', '150030', '150040', '150050', '150060', '150070', '150080', '150090', '150100', '150110', '150120', '150130', '150140', '150150', '150160', '150170', '150180', '150190', '150200', '150210', '160020', '160030', '160040', '160050', '160060', '160070', '160080', '160090', '160100', '160110', '160120', '160130', '160140', '160150', '160160', '160170', '160180', '160190', '170020', '170030', '170040', '170050', '170060', '170070', '170080', '170090', '170100', '170110', '170120', '170130', '170140', '170150', '170160', '170170', '170180', '170190', '170200', '170210', '180020', '180030', '180040', '180050', '180060', '180070', '180080', '180090', '180100', '180110', '180120', '180130', '180140', '180150', '190020', '190030', '190040', '190050', '190060', '190070', '190080', '190090', '190100', '190110', '190120', '200020', '200030', '200040', '200050', '200060', '200070', '200080', '200090', '200100', '200110', '200120', '210020', '210030', '210040', '210050', '210060', '210070', '210080', '210090', '210100', '210110', '210120', '210130', '210140', '210150', '210160', '210170', '210180', '210190', '220020', '220030', '220040', '220050', '220060', '220070', '220080', '220090', '220100', '220110', '220120', '220130', '220140', '220150', '230020', '230030', '230040', '230050', '230060', '240020', '240030', '240040', '240050', '240060', '240070', '240080', '240090', '250020', '250030', '250040', '250050', '250060', '250070', '250080', '250090', '250100', '250110', '250120', '250130', '250140', '250150', '250160', '250170', '250180', '250190', '250200', '250210', '250220', '250230', '250240', '250250', '250260', '250270', '250280', '250290', '250300', '260020', '260030', '260040', '260050', '260060', '260070', '260080', '260090', '260100', '260110', '260120', '260130', '260140', '270020', '270030', '270040', '270050', '270060', '270070', '270080', '270090', '270100', '270110', '270120', '270130', '280020', '280030', '280040', '280050', '280060', '280070', '280080', '280090', '280100', '280110', '280120', '280130', '280140', '280150', '280160', '280170', '280180', '280190', '280200', '280210', '280220', '280230', '280240', '280250', '290020', '290030', '290040', '290050', '290060', '290070', '290080', '300020', '300030', '300040', '300050', '300060', '300070', '300080', '300090', '300100', '300110', '300120', '300130', '300140', '300150', '300160', '300180', '300190', '300200', '300210', '300170', '310020', '310030', '310040', '310050', '310060', '310070', '310080', '310090', '310100', '310110', '310120', '310130', '310140', '310150', '310160', '310170', '310180']

    #成都
    #cityList = ['280020']

    #薪资类别列表
    salaList = ['10$15','15$20','20$30','30$50','50$100','100$999']

    #企业规模类别列表
    sclaList = ['010','020','030','040','050','060','070','080']

    #热门城市
    hotCityList = ['010', '020', '030', '040', '050020', '050090', '060080', '060020', '070020', '210040', '280020', '170020']

    #生成基于 不同行业,城市,薪资,规模的第一页请求
    def parse(self, response):
        for cityId in self.cityList:
            for salaId in self.salaList:
                for sclaId in self.sclaList:
                    if cityId in self.hotCityList:
                        for indusId in self.indusList:
                            full_url = self.rule_key +crate_params('0', (cityId,indusId,salaId,sclaId, '0'))
                            yield scrapy.Request(full_url,callback=self.first_parse, dont_filter=True, priority=2)

                    else:
                        full_url = self.rule_key +crate_params('1', (cityId,salaId,sclaId, '0'))
                        yield scrapy.Request(full_url,callback=self.first_parse, dont_filter=True, priority=2)
                        

    #提取第一页职位url,如果有下一页,将下一页加入请求
    def first_parse(self, response):
        #职位链接列表
        
        #posi_list = response.xpath('//div[@class="sojob-result "]//div[@class="job-info"]/h3/a/@href').extract()
        posi_list = response.xpath('//div[@class="job-info"]/h3/a/@href').extract()
        if posi_list:

            for posi in posi_list:
                posi = self.rule_key + crate_params('2', (get_num(posi),))
                yield scrapy.Request(posi,callback=self.detail_parse,priority=3)

            # 第一种:通过寻找下一页链接,循环每一页
            # next_page = response.xpath('//div[@class="sojob-result "]//div[@class="pagerbar"]/a[last()-1]/@href').extract()
            # if next_page and 'javascript:;' not in next_page:
            #     nextPage = 'https://www.liepin.com' + next_page[0]
            #     print 'next:' + nextPage
            #     yield scrapy.Request(nextPage,callback=self.first_parse)

            # 第二种:通过寻找尾页页码,循环此页码生成每一页请求
            #last_page = response.xpath('//div[@class="sojob-result "]//div[@class="pagerbar"]/a[last()]/@href').extract()


            last_page = response.xpath('//div[@class="pagerbar"]/a[last()]/@href').extract()
            
            
            if 'javascript:;' not in last_page and MORE_PAGE:
                #需要判断get参数 industries
                qs = get_qs(response.url)

                pageNum = int(last_page[0].split('=').pop())
                for num in range(1,pageNum+1):
                    cityId = qs['dqs']
                    salaId = qs['salary']
                    sclaId = qs['compscale']

                    if qs.has_key('industries'):
                        indusId = qs['industries']
                        full_url = self.rule_key +crate_params('0', (cityId,indusId,salaId,sclaId, str(num)))
                        yield scrapy.Request(full_url,callback=self.second_parse,priority=1)
                    else:
                        full_url = self.rule_key +crate_params('1', (cityId,salaId,sclaId, str(num)))
                        yield scrapy.Request(full_url,callback=self.second_parse,priority=1)

        else :
            print "=====>i didnt get any  first page"

    #处理大于1的页码页面
    def second_parse(self,response):
        #职位链接列表
        posi_list = response.xpath('//div[@class="job-info"]/h3/a/@href').extract()
        if posi_list:
            for posi in posi_list:
                posi = self.rule_key + crate_params('2', (get_num(posi),))
                yield scrapy.Request(posi,callback=self.detail_parse,priority=3)
        else:
            print "=====>i didnt get any next page"


    #职位详情页处理
    def detail_parse(self,response):

        panduan = lambda x:x[0] if x else ''
        job = LiepinItem()
        #如果是'/a/'类型网页
        if '/a/' in response.url:
            #职位名称
            job['name'] = response.xpath('//div[@class="title-info"]/h1/text() | //div[@class="title-info "]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="title-info"]/h3/text() | //div[@class="title-info "]/h3/text()').extract()[0].strip()
            #区域
            job['area'] = response.xpath('//div[@class="title"]//p[@class="basic-infor"]/span/text()').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="title"]//p[@class="job-main-title"]/text()').extract()[0].strip()
            #经验
            job['exp'] = response.xpath('//div[@class="resume clearfix"]/span[2]/text()').extract()[0]
            #学历
            job['edu'] = response.xpath('//div[@class="resume clearfix"]/span[1]/text()').extract()[0]
            #招聘人数
            job['num'] = '0'
            #发布时间
            job['time'] = response.xpath('//div[@class="job-title-left"]/p/time/text()').extract()[0].strip()
            #其他要求
            otherqlist = response.xpath('//div[@class="resume clearfix"]/span[position()>2]/text()').extract()
            job['otherq'] = ','.join(otherqlist)
            #福利
            fulis = []
            fuliList = response.xpath('//div[@class="job-main main-message"][3]//ul/li')
            for fuli in fuliList:
                fulis.append(fuli.xpath('./span/text()').extract()[0] + ':' +fuli.xpath('./text()').extract()[0])
            job['welfare'] = ','.join(fulis)
            #职位信息
            infolist = response.xpath('//div[@class="job-main main-message"][1]/div[@class="content content-word"]/text()').extract()
            job['info'] = ' '.join(infolist)
            #上班地址
            job['local'] = ''
            #公司网址
            job['co_url'] = ''
            #公司类别
            job['co_type'] = response.xpath('//div[@class="job-main main-message"][2]//ul/li[5]/text()').extract()[0]
        #如果是 '/job/'类型网页
        elif '/job/' in response.url:
            #职位名称
            job['name'] = response.xpath('//div[@class="title-info"]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="title-info"]/h3/a/text()').extract()[0].strip()
            #区域
            job['area'] = response.xpath('//div[@class="job-item"]//p[@class="basic-infor"]/span/a/text()').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="job-item"]//p[@class="job-item-title"]//text()').extract()[0].strip()
            #经验
            job['exp'] = response.xpath('//div[@class="job-qualifications"]/span[2]/text()').extract()[0]
            #学历
            job['edu'] = response.xpath('//div[@class="job-qualifications"]/span[1]/text()').extract()[0]
            #招聘人数
            job['num'] = ''
            #发布时间
            job['time'] = response.xpath('//div[@class="job-title-left"]/p/time/text()').extract()[0].strip()
            #其他要求
            otherqlist = response.xpath('//div[@class="job-qualifications"]/span[position()>2]/text()').extract()
            job['otherq'] = ','.join(otherqlist)
            #福利
            welist = response.xpath('//div[@class="tag-list"]/span/text()').extract()
            job['welfare'] = ','.join(welist)
            #职位信息
            infolist = response.xpath('//div[@class="content content-word"]//text()').extract()
            job['info'] = ' '.join(infolist)
            #上班地址
            job['local'] = response.xpath('//div[@class="company-infor"]//ul[@class="new-compintro"]//li[3]//text()').extract()[0].split('：'.decode('utf8')).pop()
            #公司网址
            job['co_url'] = response.xpath('//div[@class="company-infor"]//div[@class="company-logo"]//p/a/@href').extract()[0]
            #公司类型
            if response.xpath('//ul[@class="new-compintro"]/li[1]/a/text()').extract():
                job['co_type'] = response.xpath('//ul[@class="new-compintro"]/li[1]/a/text()').extract()[0]
            else:
                job['co_type'] = response.xpath('//ul[@class="new-compintro"]/li[1]/text()').extract()[0]
        #如果是'/cjob/'网页
        else:
            #职位名称
            job['name'] = response.xpath('//div[@class="job-title"]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="job-title"]/h2/text()').extract()[0]
            #区域
            job['area'] = response.xpath('//div[@class="job-main"]/p[@class="job-main-tip"]/span[1]/text()[2]').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="job-main"]/div[@class="job-main-title"]/strong/text()').extract()[0]
            #经验
            job['exp'] = panduan(response.xpath('//div[@class="job-main"]/p[@class="job-qualifications"]/span[2]/text()').extract())
            #学历
            job['edu'] = panduan(response.xpath('//div[@class="job-main"]/p[@class="job-qualifications"]/span[1]/text()').extract())
            #招聘人数
            job['num'] = ''
            #发布时间
            job['time'] = response.xpath('//p[@class="job-main-tip"]/span[2]/text()').extract()[0].strip()
            #其他要求
            job['otherq'] = ''
            #福利
            wellist = panduan(response.xpath('//p[@class="job-labels"]/span/text()').extract())
            job['welfare'] = ','.join(wellist)
            #职位信息
            job['info'] = response.xpath('//div[@class="job-info"]//div[@class="job-info-content"]/text()').extract()[0].strip()
            #上班地址
            job['local'] = response.xpath('//div[@class="side-box right-post-map"]/div[@class="side-content"]/p/text()').extract()[0]
            #公司网址
            job['co_url'] = ''
            #公司类型
            job['co_type'] = ''
      
        #爬虫名称
        job['spider_name'] = 'liepin'

        #识别id
        try:
            job['target_id'] = get_num(response.xpath("//link[@rel='alternate']/@href").extract()[0])
        except:
            job['target_id'] = ''

        yield job
        # #职位名称
        # print job['name']
        # #公司名称
        # print job['co_name']
        # #区域
        # print job['area']
        # #薪资
        # print job['salary']
        # #经验
        # print job['exp']
        # #学历
        # print job['edu']
        # #招聘人数
        # print job['num']
        # #发布时间
        # print job['time']
        # #其他要求
        # print job['otherq']
        # #福利
        # print job['welfare']
        # #职位信息
        # print job['info']
        # #上班地址
        # print job['local']
        # #公司网址
        # print job['co_url']
        # #公司类型
        # print job['co_type']
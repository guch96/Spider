# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from carInfo.items import BitautoCarItem
import scrapy
import re
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options
# from lxml import etree
import sys
import requests
reload(sys)
sys.setdefaultencoding("utf-8")
# def seleniumDemo(url):
#     item=BitautoCarItem()
#     options = Options()
#     options.add_argument('-headless')  # 无头参数
#     driver = webdriver.Firefox(executable_path='E:/Program Files/Mozilla Firefox/geckodriver',firefox_options=options)
#     driver.get(url)
def ReadJson():
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    response1 = requests.get("http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=baojia&pagetype=masterbrand&objid=2", headers=headers)
    result = re.findall(r'\/mb\d+\/', response1.text)
    return result
class CarinfoSpider(RedisSpider):
    name = 'carinfo'
    allowed_domains = ['bitauto.com']
    # start_urls = ['http://price.bitauto.com/mb2/',]
    redis_key = 'carspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(CarinfoSpider, self).__init__(*args, **kwargs)
    def parse(self, response):
      page_root = 'price.bitauto.com'
      page_range=ReadJson()
      for page in page_range:
          pageurl='http://'+page_root+page
          yield scrapy.Request(pageurl,callback=self.parse_item_before)
    def parse_item_before(self,response):
        print response.url
        page_root = 'price.bitauto.com'
        # treeurl = response.meta['treeurl']
        # brand = response.xpath('//div[@class ="tree_navigate"]/div/strong/text()').extract()[0]
        print "1111111"
        links=response.xpath("//div[@class='col-xs-3']//div[@class='img']/a/@href" ).extract()
        for link in links:
            page_href = link
            page_url = 'http://' + page_root + page_href
            yield scrapy.Request(page_url,callback = self.parse_car_page)

    def parse_car_page(self, response):
        page_url = response.xpath(u"//div[@class='more']/a[text()='参数']/@href").extract()[0]
        # treeurl = response.meta['treeurl']
        # brand = response.meta['brand']
        yield scrapy.Request(url=page_url, callback=self.parse_item)
    def parse_item(self,response):
           print response.url
           print 222222
           a=re.search('\[\[\[.*\]\]\]',response.body).group()
           infos=eval(a)
           for s_second in infos:
               # for s_second in s:
                   item = BitautoCarItem()
                   item['carid'] = s_second[0][0]  # "117388"
                   item['url'] = response.url
                   # item['brand'] = response.meta['brand']  ###
                   # item['treeurl'] = response.meta['treeurl']  ###
                   # item['brandurl'] = s_second[0][6]  ##changchengh5,benchieji
                   item['brandmodel4'] = s_second[0][4]  # "哈弗H5" "奔驰E级"
                   item['brandmodel5'] = s_second[0][5]  ###
                   item['version'] = s_second[0][1]  # "经典版 2.0T 手动 两驱 精英型",
                   item['image'] = s_second[0][2]
                   item['cyear'] = s_second[0][7]
                   item['ctype'] = s_second[0][12]  # "SUV"
                   item['color'] = s_second[0][13]
                   item['price1'] = s_second[1][0]  # 厂家指导价
                   item['price2'] = s_second[1][1]  # 商家报价
                   item['displacement'] = s_second[1][5]  # "2.0", 排量(L)
                   item['shiftgears'] = s_second[1][6]  # "6"
                   item['shifttype'] = s_second[1][7]  # "手动"
                   item['clength'] = s_second[2][0]  # 长宽高，为了清楚表示，加了前缀c
                   item['cwidth'] = s_second[2][1]  # 长宽高，为了清楚表示，加了前缀c
                   item['cheight'] = s_second[2][2]  # 长宽高，为了清楚表示，加了前缀c
                   item['wheelbase'] = s_second[2][3]  # 轴距
                   item['mingrounddistance'] = s_second[2][8]  # 最小离地间隙
                   item['motor'] = s_second[3][1]  # 发动机型号
                   item['intaketype'] = s_second[3][5]  # 进气形式
                   item['maxhorsepower'] = s_second[3][13]  # 最大马力(Ps)
                   item['maxpower'] = s_second[3][14]  # 最大功率(kW)
                   item['maxrpm'] = s_second[3][15]  # 最大功率转速(rpm)
                   item['oiltype'] = s_second[3][19]  # 燃料类型
                   item['oilsupply'] = s_second[3][21]  # 供油方式
                   item['tankvolume'] = s_second[3][22]  # 燃油箱容积(L)
                   item['drivetype'] = s_second[5][6]  # 驱动方式
                   item['braketype'] = s_second[5][5]  # 驻车制动类型
                   item['frontwheel'] = s_second[7][0]  # 前轮
                   item['backwheel'] = s_second[7][1]  # 后轮
                   yield item





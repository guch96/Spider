# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import *

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0']
    page_lx=LinkExtractor(allow=('start=\d+'))
    rules = (
        Rule(page_lx, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
     for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
        # 初始化模型对象
        item =  TencentspiderItem()

        item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
        # 详情连接
        item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
        # 职位类别
        typelist = each.xpath("./td[2]/text()").extract()
        if len(typelist) > 0:
            item['positionType'] = typelist[0]
        else:
            item['positionType'] = ""
        # 招聘人数
        item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
        # 工作地点
        item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
        # 发布时间
        item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

        yield item

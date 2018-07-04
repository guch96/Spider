# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentspiderItem(scrapy.Item):
    positionname = scrapy.Field()
    # 详情连接
    positionlink = scrapy.Field()
    # 职位类别
    positionType = scrapy.Field()
    # 招聘人数
    peopleNum = scrapy.Field()
    # 工作地点
    workLocation = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()

    # < a
    # href = "//car.autohome.com.cn/price/brand-32-172.html#pvareaid=2042363" > 东风汽车 < / a >
    # < a
    # href = "//car.autohome.com.cn/price/brand-1-8.html#pvareaid=2042363" > 一汽 - 大众 < / a >
    # < a
    # href = "//www.autohome.com.cn/16/#levelsource=000000000_0&amp;pvareaid=101594" > 捷达 < / a >
    # < a
    # href = "//www.autohome.com.cn/633/#levelsource=000000000_0&amp;pvareaid=101594" > 宝来 < / a >
    # < a
    # href = "//www.autohome.com.cn/82/#levelsource=000000000_0&amp;pvareaid=101594" > 途锐 < / a >
    # < a
    # href = "//car.autohome.com.cn/price/brand-1-50.html#pvareaid=2042363" > 大众(进口) < / a >
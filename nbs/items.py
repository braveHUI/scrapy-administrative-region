# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #地区代码
    area_code=scrapy.Field()
    #地区
    level=scrapy.Field()
    #地区名
    area_name=scrapy.Field()
    #全名
    full_name=scrapy.Field()
    #父类代码
    parent=scrapy.Field()

    #省份名称和url
    province_name=scrapy.Field()
    province_url=scrapy.Field()
    #市名称和url,代码
    city_name=scrapy.Field()
    city_url=scrapy.Field()
    city_code=scrapy.Field()
    #县或者区名称和url,代码

    county_name=scrapy.Field()
    county_url=scrapy.Field()
    county_code=scrapy.Field()
    #镇或者街道和url,代码
    town_name=scrapy.Field()
    town_url=scrapy.Field()
    town_code=scrapy.Field()
    #社区或乡名称和url,代码
    village_name=scrapy.Field()
    village_classify_code=scrapy.Field()
    village_code=scrapy.Field()






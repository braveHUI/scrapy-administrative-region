# -*- coding: utf-8 -*-
import scrapy
from nbs.items import NbsItem

class StatsSpider(scrapy.Spider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018'
    start_urls = [url]

    # 所有省份和直辖市的名称和url
    def parse(self, response):
        items=[]

        province_list=response.xpath("//table[@class='provincetable']/tr[@class='provincetr']/td")
        for provice in province_list:
            item=NbsItem()
            item['province_name']=provice.xpath("./a/text()").extract()[0]
            item['province_url']=provice.xpath("./a/@href").extract()[0]
            item['province_url']=self.url+'/'+item['province_url'] if len(item['province_url'])>0 else None
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['province_url'],meta={'meta_1':item},callback=self.parse_city)

    # 省份下的市的名称和url，代码
    def parse_city(self,response):
        meta_1=response.meta['meta_1']
        items=[]
        city_list=response.xpath("//table[@class='citytable']/tr[@class='citytr']")
        for city in city_list:
            item=NbsItem()
            item['city_code']=city.xpath("./td[1]/a/text()").extract()[0]
            item['city_name']=city.xpath("./td[2]/a/text()").extract()[0]
            item['city_url'] = city.xpath("./td[2]/a/@href").extract()[0]
            item['city_url']=self.url+'/'+ item['city_url'] if len( item['city_url'])>0 else None
            item['province_name']=meta_1['province_name']
            item['province_url'] = meta_1['province_url']
            #print(item)
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['city_url'],meta={"meta_2":item},callback=self.parse_county)

    # 市下的县的名称和url，代码
    def parse_county(self,response):
        meta_2 = response.meta['meta_2']
        items=[]
        county_list=response.xpath("//table[@class='countytable']/tr[@class='countytr']")
        for county in county_list:
            item=NbsItem()
            try:
                item['county_code']=county.xpath("./td[1]/a/text()").extract()[0]
                item['county_name'] = county.xpath("./td[2]/a/text()").extract()[0]
                item['county_url'] = county.xpath("./td[2]/a/@href").extract()[0]
                item['county_url']=self.url+'/'+item['county_code'][0:2]+'/'+item['county_url'] if len( item['county_url'])>0 else None
                item['province_name'] = meta_2['province_name']
                item['city_name'] = meta_2['city_name']
                item['city_code'] = meta_2['city_code']
                # 数据表中的数据
                item['area_code'] = item['county_code']
                item['level'] = "county"
                item['area_name'] = item['county_name']
                item['full_name'] = item['province_name'] + item['city_name'] + item['county_name']
                item['parent'] = item['city_code']
                yield item
                items.append(item)
            except Exception as f:
                print(f)
        for item in items:
            yield scrapy.Request(url=item['county_url'], meta={"meta_3": item}, callback=self.parse_town)

    # 县下的镇或街道的名称和url，代码
    def parse_town(self,response):
        meta_3 = response.meta['meta_3']
        items = []
        town_list=response.xpath("//table[@class='towntable']/tr[@class='towntr']")
        for town in town_list:
            item=NbsItem()
            try:
                item['town_code']=town.xpath("./td[1]/a/text()").extract()[0]
                item['town_name'] = town.xpath("./td[2]/a/text()").extract()[0]
                item['town_url'] = town.xpath("./td[2]/a/@href").extract()[0]
                item['town_url']=self.url+'/'+item['town_code'][0:2]+'/'+item['town_code'][2:4]+'/'+ item['town_url'] if len( item['town_url'])>0 else None
                item['province_name'] = meta_3['province_name']
                item['city_name'] = meta_3['city_name']
                item['city_code'] = meta_3['city_code']
                item['county_name'] = meta_3['county_name']
                item['county_code'] = meta_3['county_code']
                # 数据表中的数据
                item['area_code'] = item['town_code']
                item['level'] = "town"
                item['area_name'] = item['town_name']
                item['full_name'] = item['province_name'] + item['city_name'] + item['county_name'] + item[
                    'town_name']
                item['parent'] = item['county_code']
                yield item
                items.append(item)
            except Exception as f:
                print(f)
        for item in items:
            yield scrapy.Request(url=item['town_url'], meta={"meta_4": item}, callback=self.parse_village)

    # 镇或街道下的乡或社区的名称和分类代码，代码
    def parse_village(self, response):
        meta_4 = response.meta['meta_4']
        village_list=response.xpath("//table[@class='villagetable']/tr[@class='villagetr']")
        for village in village_list:
            item=NbsItem()
            try:
                item['village_code'] = village.xpath("./td[1]/text()").extract()[0]
                item['village_classify_code'] = village.xpath("./td[2]/text()").extract()[0]
                item['village_name'] = village.xpath("./td[3]/text()").extract()[0]
                item['province_name'] = meta_4['province_name']
                item['city_name'] = meta_4['city_name']
                item['city_code'] = meta_4['city_code']
                item['county_name'] = meta_4['county_name']
                item['county_code'] = meta_4['county_code']
                item['town_code'] = meta_4['town_code']
                item['town_name'] = meta_4['town_name']
                #数据表中的数据
                item['area_code']=item['village_code']
                item['level'] = "village"
                item['area_name'] = item['village_name']
                item['full_name'] = item['province_name']+item['city_name']+item['county_name']+item['town_name']+item['village_name']
                item['parent'] = item['town_code']
                yield item
                print(item)

            except Exception as f:
                print(f)











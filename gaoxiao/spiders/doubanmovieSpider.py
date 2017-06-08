# coding=utf-8
import sys
import scrapy
import gaoxiao.items
import json
reload(sys)
sys.setdefaultencoding('utf-8')


class doubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    baseUrl = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='
    start = 0
    start_urls = [baseUrl + str(start)]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'gaoxiao.middlewares.ProxyMiddleWare': 1
        },
        'ITEM_PIPELINES': {
            'gaoxiao.pipelines.CnblogImagesPipeline': 1,
        }
    }

    def parse(self, response):
        data = json.loads(response.text)['subjects']
        for i in data:
            item = gaoxiao.items.CnblogImageItem()
            if i['cover'] != '':
                item['image'] = i['cover']
                item['name'] = i['title']
            else:
                item['image'] = ''
            yield item
        if len(data) > 0:
            self.start += 20
            yield scrapy.Request(self.baseUrl + str(self.start), callback=self.parse)

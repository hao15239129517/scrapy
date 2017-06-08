# coding=utf-8
import sys
import scrapy
import gaoxiao.items
reload(sys)
sys.setdefaultencoding('utf-8')


class GaoXiaoSpider(scrapy.Spider):
    name = 'gaoxiaosp'
    allowed_domains = ['gkcx.eol.cn']
    baseUrl = 'http://gkcx.eol.cn/soudaxue/queryschool.html?&page='
    page = 1
    start_urls = [baseUrl + str(page)]
    custom_settings = {'DOWNLOADER_MIDDLEWARES': {
        'gaoxiao.middlewares.ProxyMiddleWare': 1,
        'gaoxiao.middlewares.GaoxiaoSpiderMiddleware': 3
    }, 'ITEM_PIPELINES': {
        'gaoxiao.pipelines.GaoxiaoPipeline': 1,
    }
    }

    def parse(self, response):
        list = response.xpath("//tbody[@class='lin-seachtable']/tr")
        for i in list:
            gaoxiaoItem = gaoxiao.items.GaoxiaoItem()
            gaoxiaoItem['name'] = i.xpath("./td[1]/a/text()").extract()[0]
            gaoxiaoItem['province'] = i.xpath("./td[2]/text()").extract()[0]
            if len(i.xpath("./td[3]/text()").extract()) > 0:
                gaoxiaoItem['college'] = i.xpath("./td[3]/text()").extract()[0]
            else:
                gaoxiaoItem['college'] = ''
            yield gaoxiaoItem
        if len(list) > 0:
            self.page += 1
            yield scrapy.Request(self.baseUrl + str(self.page), callback=self.parse)

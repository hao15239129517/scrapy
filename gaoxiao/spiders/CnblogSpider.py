# coding=utf-8
import sys
import scrapy
import gaoxiao.items
reload(sys)
sys.setdefaultencoding('utf-8')


class CnblogSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com', 'pic.cnblogs.com']
    baseUrl = 'https://www.cnblogs.com/sitehome/p/'
    page = 1
    start_urls = [baseUrl + str(page)]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'gaoxiao.middlewares.ProxyMiddleWare': 1,
            'gaoxiao.middlewares.GaoxiaoSpiderMiddleware': 544
        },
        'ITEM_PIPELINES': {
            'gaoxiao.pipelines.CnblogImagesPipeline': 1,
        }
    }

    def parse(self, response):

        for i in response.xpath("//div[@id='post_list']/div"):
            item = gaoxiao.items.CnblogImageItem()
            if len(i.xpath("./div[@class='post_item_body']//img/@src").extract()) > 0:
                item['image'] = i.xpath(
                    "./div[@class='post_item_body']//img/@src").extract()[0]
            else:
                item['image'] = ''
            item['name'] = i.xpath(
                "./div[@class='post_item_body']/div[@class='post_item_foot']//a/text()").extract()[0]
            yield item
        if self.page < 200:
            self.page += 1
            yield scrapy.Request(self.baseUrl + str(self.page), callback=self.parse)

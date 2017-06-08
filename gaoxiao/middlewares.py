# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')


class GaoxiaoSpiderMiddleware(object):

    def process_request(self, request, spider):
        if len(request.flags) > 0 and request.flags[0] == 'img':
            return None
        driver = webdriver.PhantomJS()
        # 设置全屏
        driver.maximize_window()
        driver.get(request.url)
        content = driver.page_source
        driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=content)


class ProxyMiddleWare(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://124.163.67.177:8998'

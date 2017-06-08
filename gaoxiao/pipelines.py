# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt
import scrapy
import hashlib
import scrapy.utils
import os
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

import gaoxiao.items


class GaoxiaoPipeline(object):

    def __init__(self):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet(u'全国高校汇总')
        self.count = 0

    def process_item(self, item, spider):
        if isinstance(item, gaoxiao.items.GaoxiaoItem):
            self.ws.write(self.count, 0, item['name'])
            self.ws.write(self.count, 1, item['province'])
            self.ws.write(self.count, 2, item['college'])
            self.count = self.count + 1
            return item

    def close_spider(self, spider):
        self.wb.save(u'全国高校.xls')


class CnblogImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        image_url = item['image']
        if image_url != '':
            if not image_url.startswith('http'):
                image_url = 'http://' + str(image_url)
            if not item.__contains__('name'):
                item['name'] = ''
            yield scrapy.Request(image_url, meta={'name': item['name']}, flags=['img', item['name']])

    def file_path(self, request, response=None, info=None):
        # 源码  文件名 对url地址取hash值

        name = request.meta['name']

        if name == '' or name.find('*') >= 0 or name.find('?') >= 0 or name.find('\\') >= 0 or name.find('/') >= 0 or name.find('<') >= 0 or name.find('>') >= 0 or name.find(':') >= 0 or name.find('"') >= 0 or name.find('|') >= 0:
            name = hashlib.sha1(
                scrapy.utils.python.to_bytes(request.url)).hexdigest()
        imagePath = name + '.' + \
            request.url.split('/')[-1].split('.')[-1].split('?')[0]
        return imagePath

    def item_completed(self, result, item, info):
        image_path = [x["path"] for ok, x in result if ok]
        if image_path:
            item["imagePath"] = image_path
        else:
            item['imagePath'] = ''

        return item

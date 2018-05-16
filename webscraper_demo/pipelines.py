# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Define your item pipelines here
#
import MySQLdb
import scrapy
from scrapy import log
from twisted.enterprise import adbapi
import csv
from time import gmtime, strftime
# import MySQLdb.cursors
from testmodels.models import TestModels
from testmodels import const
from scrapy.pipelines.images import ImagesPipeline

# Database storage pipeline. Adapted from Scrapy docs
# Connects to a MySQL database via a connection pool to allow
# for non blocking DB access

from webcrawling.models import Select, Items


class DbProductCountPipeline(object):

    def process_item(self,item,spider):
        if item:
            if ('all_product_count' and 'find_product_count' and 'fail_product_count') in item :
                # query = "UPDATE tbl_product_count SET all_product_count=%s, find_product_count=%s, fail_product_count=%s where id=%s"
                db = MySQLdb.connect(host="192.168.8.118",
                                       user="root",
                                       passwd="",
                                       db="django")
                cursor = db.cursor()
                data = (item['all_product_count'],item['find_product_count'],item['fail_product_count'],1)
                # tx.execute(query, data)
                cursor.execute("UPDATE tbl_product_count SET all_product_count=%s, find_product_count=%s, fail_product_count=%s where id=%s" % data)
                db.commit()
                cursor.close()
        return item



class ItemsAndSelectPipeline(object):

    def process_item(self,item,spider):
        if item:
            if ('productId' and 'product_name' and 'category_name' and 'prodURL' and 'categoryId' and 'category_set_name' and 'brand_name' and 'price' and 'prodDescription' and 'prodImgURL' and 'selectedColor' and 'balance' and 'selType') in item:
                row = ['', item['productId'], item['product_name'], item['category_name'], '', item['prodURL'], '',
                        item['category_set_num'], item['category_set_name'], item['brand_name'],
                        item['price'], item['prodDescription'], item['prodImgURL'], item['selectedColor'],
                        item['balance'], item['selType']]
                product = Items.objects.filter(field2 = item['productId']).exists()
                if (product == True):
                    update_product = Items.objects.get(field2 = item['productId'])
                    update_product.field1 = ''
                    update_product.field3 = item['product_name']
                    update_product.field4 = item['category_name']
                    update_product.field5 = ''
                    update_product.field6 = item['prodURL']
                    update_product.field7 = ''
                    update_product.field8 = item['category_set_num']
                    update_product.field9 = item['category_set_name']
                    update_product.field10 = item['brand_name']
                    update_product.field11 = item['price']
                    update_product.field12 = item['prodDescription']
                    update_product.field13 = item['prodImgURL']
                    update_product.field14 = item['selectedColor']
                    update_product.field15 = item['balance']
                    update_product.field16 = item['selType']
                    update_product.action = 'u'
                    update_product.count = '1'
                    update_product.save()

                else:
                    insert_product = Items(
                        field1 = '',
                        field2 = item['productId'],
                        field3 = item['product_name'],
                        field4 = item['category_name'],
                        field5 = '',
                        field6 = item['prodURL'],
                        field7 = '',
                        field8 = item['category_set_num'],
                        field9 = item['category_set_name'],
                        field10 = item['brand_name'],
                        field11 = item['price'],
                        field12 = item['prodDescription'],
                        field13 = item['prodImgURL'],
                        field14 = item['selectedColor'],
                        field15 = item['balance'],
                        field16 = item['selType'],
                        action  = 'i',
                        count   = '1'
                    )
                    insert_product.save()
                log.msg("write item in Items DB", level=log.DEBUG)
            if ('productId' and 'select_list') in item:

                Select.objects.filter(field2=item['productId']).delete()
                for row in item['select_list']:
                    insert_select = Select(
                        field1 = row[0],
                        field2 = row[1],
                        field3 = row[2],
                        field4 = row[3],
                        field5 = row[4],
                        field6 = row[5],
                        field7 = row[6],
                        field8 = row[7],
                        field9 = row[8],
                        field10 = row[9],
                        field11 = row[10],
                        field12 = row[11],
                        field13 = row[12],
                        field14 = row[13],
                        field15 = row[14],
                        field16 = row[15],
                        field17 = row[16],
                    )
                    insert_select.save()
                log.msg("Select is stored in Select db", level=log.DEBUG)
        return item
class dlImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # use 'accession' as name for the image when it's downloaded
        return [scrapy.Request(x, meta={'image_name': item["productId"]})
                for x in item.get('image_urls', [])]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        image_name = str(request.meta['image_name'])
        return '%s.jpg' % image_name
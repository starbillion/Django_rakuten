# -*- coding: utf-8 -*-
import scrapy
from webscraper_demo.items import WebscraperDemoItem
import re
from testmodels.models import TestModels
from testmodels import const
import json
from scrapy.http import FormRequest
from scrapy.selector import Selector
import base64
import time

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'test2'
    base_url = "http://www.neimanmarcus.com"
    first_url = "http://www.neimanmarcus.com/en-jp/Designers/cat000730/c.cat"
    find_type = 0
    cur_alphaindex = 0
    cur_linkindex = 0
    all_product_count = 0
    find_product_count = 0
    fail_product_count = 0
    page_size =120

    def start_requests(self):
        tmp = TestModels.get_test2_data()
        self.find_type = int(tmp[0])
        self.cur_alphaindex =int(tmp[1])
        self.cur_linkindex =int(tmp[2])
        # self.find_type = 0
        # self.cur_alphaindex = 0
        # self.cur_linkindex = 22
        url = self.first_url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        indexgroups=response.xpath('//div[@class="indexgroup gutter-bottom"]')
        if self.cur_alphaindex< len(indexgroups):
            indexgroup =indexgroups [self.cur_alphaindex]
            # '//div[@class="designerList"]//div//div[@class="designerlink"]//a/@href'
            pageSize = '&pageSize='+ str(self.page_size)
            groups = indexgroup.xpath('.//a[contains(@href, "en-jp")]/@href').extract()
            if self.cur_linkindex < len(groups):
                href = groups[self.cur_linkindex]
                url =self.base_url + href + pageSize
                url1 = self.base_url + href
                TestModels.set_find_type(const.FIND_PROGRESS)
                yield scrapy.Request(url=url, callback = self.parse_designerlink, meta={'type': 0,'url1':url1,'items_count':0,'find_count':0,'page_num':0},errback=self.parse_designerlink_err)
            else:
                self.cur_linkindex = 0
                self.cur_alphaindex += 1
                TestModels.set_test2_index_data(self.cur_alphaindex, self.cur_linkindex)
                yield self.parse(response)

        else:
            TestModels.set_find_type(const.FIND_SUCCESS)

    def parse_designerlink_err(self):
        TestModels.set_find_type(const.FIND_ERROR)

    def parse_designerlink(self, response):
        if response.meta['type'] == 2:
            json_data = json.loads(response.body)
            sel = Selector(text=json_data.get('GenericSearchResp', '').get('productResults',''))
            numItems = [0]
        else:
            navLastItem = response.xpath('//a[contains(@class,"navLastItem")]/@href').extract()
            numItems = response.xpath('//span[@id="numItems"]/text()').extract()
        if len(numItems)>0 :
            items_count = response.meta['items_count']
            find_count = response.meta['find_count']
            page_num = response.meta['page_num']
            if int(response.meta['type']) == 0:
                items_count = int(numItems[0])
                self.all_product_count += items_count
                find_count = 0
                page_num = 0
            if response.meta['type'] == 2:
                productList = sel.xpath('//a[@id="productTemplateId"]/@href').extract()
            else:
                productList = response.xpath('//a[@id="productTemplateId"]/@href').extract()
            for href in productList:
                url = self.base_url + href
                find_count += 1
                yield scrapy.Request(url=url, callback=self.parse_product, meta={'data':url}, errback=self.parse_product_fail)
            if find_count < items_count:
                page_num += 1
                catId ='cat'+ str(re.search(r"\/cat(.*?)_cat",response.meta['url1']).groups()[0])
                tmp='{"GenericSearchReq":{"pageOffset":'+ str(page_num)\
                    + ',"pageSize":"'+ str(self.page_size)\
                    +'","refinements":"","selectedRecentSize":"","activeFavoriteSizesCount":"0","activeInteraction":"true","mobile":false,"sort":"","personalizedPriorityProdId":"x","endecaDrivenSiloRefinements":"navAction=index","definitionPath":"/nm/commerce/pagedef_rwd/template/EndecaDrivenHome","userConstrainedResults":"true","updateFilter":"false","rwd":"true","advancedFilterReqItems":{"StoreLocationFilterReq":[{"allStoresInput":"false","onlineOnly":""}]},"categoryId":"'\
                    + catId +'","sortByFavorites":false,"isFeaturedSort":true,"prevSort":""}}'
                # s = json.dumps(tmp)
                tmp1="$b64$" + base64.b64encode(tmp)
                data=tmp1.replace("=", "$")
                # tmp ='#endecaDrivenSiloRefinements=navAction%3Dindex&personalizedPriorityProdId=x&userConstrainedResults=true&refinements=&page='+\
                #      str(page_num)+'&pageSize='+ str(self.page_size)+\
                #      '&sort=&definitionPath=/nm/commerce/pagedef_rwd/template/EndecaDrivenHome&onlineOnly=&updateFilter=false&allStoresInput=false&rwd=true&catalogId=cat'+\
                #      catId +'&selectedRecentSize=&activeFavoriteSizesCount=0&activeInteraction=true'
                # url=response.meta['url1'] + tmp
                #
                # yield scrapy.Request(url=url,dont_filter=True, callback = self.parse_designerlink, meta={'type': 1,'url1':response.meta['url1'],'items_count':items_count,'find_count':find_count,'page_num':page_num})
                post_url = self.base_url + "/en-jp/category.service"
                timestamp=str(time.time()*1000)
                # '$b64$eyJHZW5lcmljU2VhcmNoUmVxIjp7InBhZ2VPZmZzZXQiOjEsInBhZ2VTaXplIjoiMTIwIiwicmVmaW5lbWVudHMiOiIiLCJzZWxlY3RlZFJlY2VudFNpemUiOiIiLCJhY3RpdmVGYXZvcml0ZVNpemVzQ291bnQiOiIwIiwiYWN0aXZlSW50ZXJhY3Rpb24iOiJ0cnVlIiwibW9iaWxlIjp0cnVlLCJzb3J0IjoiIiwicGVyc29uYWxpemVkUHJpb3JpdHlQcm9kSWQiOiJ4IiwiZW5kZWNhRHJpdmVuU2lsb1JlZmluZW1lbnRzIjoibmF2QWN0aW9uPWluZGV4IiwiZGVmaW5pdGlvblBhdGgiOiIvbm0vY29tbWVyY2UvcGFnZWRlZl9yd2QvdGVtcGxhdGUvRW5kZWNhRHJpdmVuSG9tZSIsInVzZXJDb25zdHJhaW5lZFJlc3VsdHMiOiJ0cnVlIiwidXBkYXRlRmlsdGVyIjoiZmFsc2UiLCJyd2QiOiJ0cnVlIiwiYWR2YW5jZWRGaWx0ZXJSZXFJdGVtcyI6eyJTdG9yZUxvY2F0aW9uRmlsdGVyUmVxIjpbeyJhbGxTdG9yZXNJbnB1dCI6ImZhbHNlIiwib25saW5lT25seSI6IiJ9XX0sImNhdGVnb3J5SWQiOiJjYXQxMDIzMDczOSIsInNvcnRCeUZhdm9yaXRlcyI6ZmFsc2UsImlzRmVhdHVyZWRTb3J0Ijp0cnVlLCJwcmV2U29ydCI6IiJ9fQ$$'
                formdata = {'data': data,
                            'service':'getCategoryGrid',
                               'sid':'getCategoryGrid',
                            'bid':'GenericSearchReq',
                            'timestamp':timestamp}
                yield FormRequest(url=post_url, formdata=formdata, callback=self.parse_designerlink,meta={'type': 2,'url1':response.meta['url1'],'items_count':items_count,'find_count':find_count,'page_num':page_num})
        else:
            if len(navLastItem)>0:
                # for href in navLastItem:
                pageSize = '?pageSize=' + str(self.page_size)
                for href in navLastItem:
                    url = self.base_url + href + pageSize
                    url1 = self.base_url + href
                    yield scrapy.Request(url=url, callback = self.parse_designerlink, meta={'type': 0,'url1':url1,'items_count':0,'find_count':0,'page_num':0})
    def parse_product_fail(self):
        self.fail_product_count += 1
        item = WebscraperDemoItem()
        item['all_product_count'] = self.all_product_count
        item['find_product_count'] = self.find_product_count
        item['fail_product_count'] = self.fail_product_count

    def parse_product(self, response):
        self.find_product_count += 1
        def extract_var(reg):
            return response.xpath('//script').re(reg)

        prodURL = response.meta['data'].encode('utf-8')

        prodInfo = json.loads((extract_var(r"window.utag_data=(.*?);"))[0])
        productId = (prodInfo["product_id"])[0].encode('utf-8')
        product_name = (prodInfo["product_name"])[0].encode('utf-8')
        categoryId = (prodInfo["cat_id"])[len(prodInfo["cat_id"]) - 1]
        categoryList = (json.loads((extract_var(r"window.utag_data=(.*?);"))[0]))["bread_crumb"]
        category_name = ""
        category_set_name = ""
        for k in range(len(categoryList)):
            if k == 0:
                category_set_name = categoryList[k].encode('utf-8')
            if k == len(categoryList) - 1:
                category_name = category_name + categoryList[k].encode('utf-8')
            else:
                category_name = category_name + categoryList[k].encode('utf-8') + "\\"

        prodImgURL = (response.xpath('//div[@id="prod-img"]//img/@src').extract()[0]).encode('utf-8')

        prodDetailInfo = response.xpath('//div[@class="productCutline"]')[0]
        prodDescription = []
        prodInfoList = prodDetailInfo.xpath('.//ul//text()').extract()
        for j in range(len(prodInfoList)):
            prodDescription.append(prodInfoList[j].encode('utf-8'))
        # print(prodDescription)
        temp_price = response.xpath('//p[contains(@class, "product-price")]/text()').extract()
        if len(temp_price) > 0:
            price = temp_price[0].encode('utf-8')
        else:
            price = response.xpath('//span[contains(@class, "item-price")]/text()').extract()[0].encode('utf-8')
        item = WebscraperDemoItem()
        item['all_product_count'] = self.all_product_count
        item['find_product_count'] = self.find_product_count
        item['fail_product_count'] = self.fail_product_count

        item['productId'] = productId
        item['product_name'] = product_name
        item['category_name'] = category_name
        item['prodURL'] = prodURL
        item['categoryId'] = categoryId
        item['category_set_name'] = category_set_name
        item['brand_name'] = ""
        item['price'] = price
        item['prodDescription'] = prodDescription
        item['prodImgURL'] = prodImgURL
        yield item
    def parse_product_err(self):
        self.fail_product_count += 1
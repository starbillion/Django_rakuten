# -*- coding: utf-8 -*-
import scrapy
import csv
from webscraper_demo.items import WebscraperDemoItem
from scrapy import signals

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'test'
    base_url = "http://www.zappos.com"
    first_url = "http://www.zappos.com/null/.zso?p="
    page_num = 0
    p_count = 0
    find_count = 0
    # field = [u'コントロールカラム', u'商品管理番号（商品ID）', u'商品名', u'表示先カテゴリ', u'優先度', u'商品URL', u'1ページ複数形式', u'カテゴリセット管理番号',
    #          u'カテゴリセット名', u'ブランド名', u'販売価格', u'商品説明文', u'商品画像URL']
    # with open("item.csv", "wb") as fp:
    #     fp.truncate()
    #     fp.write(u'\ufeff'.encode('utf8'))
    #     wr = csv.writer(fp, dialect='excel')
    #     wr.writerow([item.encode('utf-8') for item in field])
    #     fp.close()

    def start_requests(self):
        url = self.first_url + str(self.page_num)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.page_num is 0:
            self.p_count = int( response.xpath('//em/text()').extract_first())
            # yield { "product_count": self.p_count}

        for href in response.xpath('//div[@id="searchResults"]//a/@href').extract():
            url =self.base_url + href
            yield response.follow(url, self.parse_product, meta={'data': url})
        if self.find_count < self.p_count:
            self.page_num += 1
            url = self.first_url + str(self.page_num)
            yield scrapy.Request(url=url, callback=self.parse)
    def parse_product(self, response):
        prodURL =response.meta['data'].encode('utf-8')
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        def extract_var(reg):
            return response.xpath('//script').re(reg)
        self.find_count += 1
        breadcrumbs = response.xpath('//div[@id="breadcrumbs"]//a/text()').extract()
        price = (response.xpath('//span[contains(@class, "nowPrice") or contains(@class, "salePrice")]/text()').extract())[0].encode('utf-8')
        # print(price)
        category_name = ''
        category_set_name = ''
        for i in range(len(breadcrumbs)):
            if i == 0:
                continue
            if i == len(breadcrumbs) - 2:
                category_name += breadcrumbs[i]
            elif i < len(breadcrumbs) - 2:
                category_name += breadcrumbs[i] + "\\"
        if len(breadcrumbs) > 1:
            category_set_name = breadcrumbs[1]
        brand_name = ''
        brand_name = ((extract_var(r"var brandName = (.*?);"))[0].encode('utf-8')).replace('"', '')
        # print(category_name)
        # print(category_set_name)
        # print(brand_name)
        #print(self.find_count)
        item = WebscraperDemoItem()
        item['product_count'] = self.p_count
        item['find_count'] = self.find_count

        product_name = ((extract_var(r"var productName = (.*?);"))[0].encode('utf-8')).replace('"', '')
        # print(product_name)
        productId = (extract_var(r"var productId = (.*?);"))[0].encode('utf-8')
        # print(productId)
        categoryId = (extract_var(r"var categoryNum = (.*?);"))[0].encode('utf-8')
        # print(categoryId)
        prodImgURL = (response.xpath('//div[@class="actor"]//img/@src').extract()[0]).encode('utf-8')
        # print(prodImgURL)
        prodInfoList = response.xpath('//div[@class="description"]//ul').extract()
        prodDescription = []
        prodInfoList = response.xpath('//div[@class="description"]//ul//li/text()').extract()
        for j in range(len(prodInfoList)):
            prodDescription.append(prodInfoList[j].encode('utf-8'))

        item['productId']=productId
        item['product_name']=product_name
        item['category_name']=category_name
        item['prodURL']=prodURL
        item['categoryId']=categoryId
        item['category_set_name']=category_set_name
        item['brand_name']=brand_name
        item['price']=price
        item['prodDescription']=prodDescription
        item['prodImgURL']=prodImgURL
        yield item
        # with open("item.csv", "ab") as fp1:
        #     wr1 = csv.writer(fp1, dialect='excel')
        #     wr1.writerow(['', productId, product_name, category_name, '', prodURL, '', categoryId, category_set_name, brand_name, price, prodDescription, prodImgURL])
        #
        #     yield {
        #         'product Name': product_name,
        #         'product Id': productId,
        #         'category Name': category_name,
        #         'category Set Name': category_set_name,
        #         'brand name': brand_name,
        #     }

    @classmethod
    def get_find_count(self):
        return self.find_count

    @classmethod
    def get_product_count(self):
        return self.p_count
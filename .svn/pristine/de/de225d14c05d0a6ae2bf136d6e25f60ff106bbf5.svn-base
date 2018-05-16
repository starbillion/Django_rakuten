# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from django.http import HttpResponse
from scrapy import signals, FormRequest, log
from testmodels.models import TestModels
from testmodels import const

class WebscraperDemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        yield exception
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        status = const.STATUS_ON
        TestModels.set_status(status)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        status = const.STATUS_OFF
        TestModels.set_status(status)

        url = 'http://192.168.8.118/start'
        tmp = TestModels.get_find_count()
        all_p_count = tmp[0]
        find_p_count = tmp[1]
        fail_p_count = tmp[2]
        tmp = TestModels.get_test2_data()
        find_type = tmp[0]
        status = tmp[4]
        data = {
            'result': "SUCCESS",
            "content": {
                "all": all_p_count,
                "find": find_p_count,
                "fail": fail_p_count,
                "find_type": find_type,
                "status": status,
            }
        }
        log.msg("Ended crawling products.........", level=log.DEBUG)
        #yield FormRequest(url=url, formdata=data)
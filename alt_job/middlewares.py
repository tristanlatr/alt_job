from scrapy import Request
try: 
    from scrapy_selenium import SeleniumMiddleware as SeleniumMiddlewareBase
    from scrapy_selenium import SeleniumRequest
except ImportError: 
    SeleniumMiddlewareBase=object
    SeleniumRequest=Request
import time
import random

# Extends Selenium to respect scrapy config https://github.com/clemfromspace/scrapy-selenium/issues/36
class SeleniumMiddleware(SeleniumMiddlewareBase):
    def process_request(self, request, spider):
        if isinstance(request, SeleniumRequest):
            delay = spider.settings.getint('DOWNLOAD_DELAY')
            randomize_delay = spider.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
            if delay:
                if randomize_delay:
                    delay = random.uniform(0.5 * delay, 1.5 * delay)
                time.sleep(delay)
        try: return super().process_request(request, spider)
        except AttributeError: return None
#    SCRAPY TOR MIDLEWARE
# https://github.com/elvesrodrigues/scrapy-tor-proxy-rotation


# # Define here the models for your spider middleware
# #
# # See documentation in:
# # https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals

# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter

# import os
# import stem
# import stem.control

# def _set_new_ip():
#     with stem.control.Controller.from_port(port=9051) as controller:
#         controller.authenticate(password='tor_password')
#         controller.signal(stem.Signal.NEWNYM)

# class TorMiddleware(object):
#     """
#     NOT USED 
#     You must first install the Tor service on your system
#     """
#     def process_request(self, request, spider):
#         _set_new_ip()
#         request.meta['proxy'] = 'http://127.0.0.1:8118'
#         spider.log('Proxy : %s' % request.meta['proxy'])

# #   TODO: ENABLE MIDDLEWARE ONLY IF CONFIG FILE OPTION IS ON AND SITE 
# #   IS NOT PROTECTED BY CLOUDFLARE (=> MAKE A CONSTANT OF CLOUD FLARE PROTECTED SITES)


# class AltJobSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


# class AltJobDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)

from scrapy import signals
import os
from stem import Signal
from stem.control import Controller

def _set_new_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='tor_password')
        controller.signal(Signal.NEWNYM)

class TorMiddleware(object):
    """
    You must first install the Tor service on your system
    """
    def process_request(self, request, spider):
        _set_new_ip()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log('Proxy : %s' % request.meta['proxy'])

#TODO:ENABLE MIDDLEWARE ONLY IF CONFIG FILE OPTION IS ON AND SITE 
#   IS NOT PROTECTED BY CLOUDFLARE (=> MAKE A CONSTANT OF CLOUD FLARE PROTECTED SITES)
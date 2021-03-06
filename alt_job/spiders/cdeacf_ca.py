import scrapy
import urllib
import tempfile
from .base import Scraper
from ..items import Job

class Scraper_cdeacf_ca(Scraper):
    name = "cdeacf.ca"
    allowed_domains = ["webcache.googleusercontent.com", name]
    start_urls = ["http://cdeacf.ca/recherches?f%5B0%5D=type%3Aoffre_demploi"]

    def parse(self, response):
        """
        @auto_url cdeacf.ca
        @returns items 20 20
        @scrape_not_none url date_posted organisation title apply_before location
        """
        return super().parse(response)

    def get_jobs_list(self, response):
        """
        @auto_url cdeacf.ca
        @returns_valid_selectorlist
        """
        # HTML <ul> contains all li of postings
        return response.xpath('//div[@id="main-content"]//div[@class="view-content"]/div/ul/li')

    def get_job_dict(self, selector):
        return {
            'url':urllib.parse.urljoin('http://cdeacf.ca/', selector.xpath('div[contains(@class,"views-field-title")]//a/@href').get()),
            'date_posted':selector.xpath('div[contains(@class,"views-field-created")]//span[@class="field-content-inner"]/text()').get(),
            'organisation':selector.xpath('div[contains(@class,"views-field-field-organisme")]//span[@class="field-content"]/text()').get(),
            'title':selector.xpath('div[contains(@class,"views-field-title")]//a/text()').get(),
            'apply_before': selector.xpath('div[9]/span[2]/span/text()').get(),
            'location': selector.xpath('div[8]/span/text()').get()
        }
    
    def get_next_page_url(self, response):
        """
        @auto_url cdeacf.ca
        @returns_valid_link
        """
        return urllib.parse.urljoin('http://cdeacf.ca/', response.xpath('//*[@id="block-system-main"]/div/div[2]/ul/li[contains(@class,"pager-next")]/a/@href').get())

    def parse_full_job_page(self, response, job_dict):
        """
        @auto_job_url cdeacf.ca
        @scrape_not_none url title description
        @returns items 1 1  
        """
        main_job_link_url=response.xpath('//article[contains(@class,"node-offre-demploi")]//a/@href').get()
        # PDF detection
        if main_job_link_url.lower().endswith('.pdf'):
            try: 
                import pdfplumber
                import requests
            except ImportError:
                job_dict['description']='{}'.format(main_job_link_url)
            else:    
                r = requests.get(main_job_link_url, stream=True)
                with tempfile.NamedTemporaryFile('wb') as f:
                    f.write(r.content)
                    with pdfplumber.open(f.name) as pdf:
                        job_dict['description']='\n\n'.join([p.extract_text() for p in pdf.pages])
        else:
            job_dict['description']='{}'.format(main_job_link_url)
        return Job(job_dict)
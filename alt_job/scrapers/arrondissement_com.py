import scrapy
from bs4 import BeautifulSoup
import alt_job.scrapers
from alt_job.jobs import Job

class Scraper_arrondissement_com(alt_job.scrapers.Scraper):
    name = "arrondissement.com"
    allowed_domains = ["webcache.googleusercontent.com", name]
    
    def get_jobs_list(self, response):
        # HTML <div class="listing"> contains all dic of postings
        return response.xpath('//div[@class="listing"]').xpath('div')

    def get_job_dict(self, selector):
        return {
            'url':selector.css('a::attr("href")').get(),
            'date_posted':selector.css('div::text').get(),
            'organisation':selector.xpath('a[@class="fromDirLink"]/text()').get(),
            'title':selector.xpath('a[@class="title"]/text()').get()
        }

    def parse_full_job_page(self, response, job_dict):
        job_dict['description']=BeautifulSoup(response.xpath('//div[@id="fiche"]/div[@class="publication"]').get()).get_text()
        return self.check_regex(Job(job_dict))
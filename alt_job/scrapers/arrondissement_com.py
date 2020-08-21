from bs4 import BeautifulSoup
import alt_job.scrapers
from alt_job.jobs import Job

class Scraper_arrondissement_com(alt_job.scrapers.Scraper):
    name = "arrondissement.com"
    allowed_domains = ["webcache.googleusercontent.com", name]
    
    def get_jobs_list(self, response):
        # HTML <div class="listing"> contains all dic of postings
        return response.xpath('//div[contains(@class,"listing")]/div')

    def get_job_dict(self, selector):
        return {
            'url':selector.xpath('a/@href').get(),
            'date_posted':selector.xpath('text()').get(),
            'organisation':selector.xpath('a[@class="fromDirLink"]/text()').get(),
            'title':selector.xpath('a[@class="title"]/text()').get()
        }

    def parse_full_job_page(self, response, job_dict):
        job_dict['description']=BeautifulSoup(response.xpath('//div[@id="fiche"]/div[contains(@class,"publication")]').get()).get_text()
        job_dict['apply_before']=response.xpath('//*[@id="fiche"]/div[2]/div[2]/div[6]/text()').get()
        job_dict['job_type']=response.xpath('//*[@id="fiche"]/div[2]/div[2]/div[4]/text()').get()
        job_dict['week_hours']=response.xpath('//*[@id="fiche"]/div[2]/div[2]/div[2]/text()').get()
        job_dict['salary']=response.xpath('//*[@id="fiche"]/div[2]/div[2]/div[3]/text()').get()
        return Job(job_dict)

    def get_next_page_url(self, response):
        return response.xpath('//table[contains(@class,"pager-nav")]//tr/td[last()]/a/@href').get()
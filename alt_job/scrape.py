"""
Wrapper arround scrapy system and scrapy related helpers
"""

import json
import tempfile
import os
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import spiderloader
import scrapy.settings

def get_alt_job_settings():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'alt_job.settings')
    settings=get_project_settings()
    return settings

def get_all_scrapers():
    spider_loader = spiderloader.SpiderLoader(settings=get_alt_job_settings())
    spiders = spider_loader.list()
    return spiders

def scrape(website, scraper_config, log_level='ERROR', db=None):
    """
    Wrap the crawling procress in multiprocessing thread.  
    """
    scraped_data_result=multiprocessing.Manager().list()
    process = multiprocessing.Process(target=_scrape,
        kwargs=dict(website=website,
            scraper_config=scraper_config,
            db=db,
            log_level=log_level,
            scraped_data_result=scraped_data_result))
    process.start()
    process.join()
    scraped_data_result=list(scraped_data_result)
    return scraped_data_result

def _scrape(website, scraper_config, log_level, scraped_data_result=None, db=None):
    """
    Launch the requested scraper with the configuration.  
    """
    scraped_data_result=[] if scraped_data_result==None else scraped_data_result
    scrapy_process_json_data=None

    with tempfile.NamedTemporaryFile() as scrapy_process_temp_file:
        settings=get_alt_job_settings()
        settings.set("FEEDS", {
                '{}'.format(scrapy_process_temp_file.name): {
                    'format': 'json',
                    'encoding': 'utf8',
                    'indent': 4
                }})
        settings.set("LOG_LEVEL", log_level)
        # Scrapy configuration, launched with temp file
        process = CrawlerProcess(settings=settings)
        process.crawl(website, **scraper_config, db=db)
        process.start()
        
        with open(scrapy_process_temp_file.name, 'r', encoding='utf-8') as crawler_process_json_fp:
            try:
                scrapy_process_json_data=json.load(crawler_process_json_fp)
                # write result in argument's list, used with multiprocessing
                scraped_data_result.extend(scrapy_process_json_data)
                return(scrapy_process_json_data)

            except ValueError as err:
                if str(crawler_process_json_fp.read()).strip()=="":
                    raise ValueError('Looks like there has been an issue during the scrape, no data is found in scrapy feed.\nReport this issue on github!') from err
                else:
                    raise
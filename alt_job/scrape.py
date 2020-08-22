import json
import tempfile
from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
import scrapy.settings

def get_all_scrapers():
    spider_loader = spiderloader.SpiderLoader(settings=scrapy.settings.Settings(values={"SPIDER_MODULES":"alt_job.scrapers"}))
    spiders = spider_loader.list()
    return spiders

def scrape(website, scraper_config, log_level, scraped_data_result=None, db=None):
    scraped_data_result=[] if scraped_data_result==None else scraped_data_result
    scrapy_process_json_data=None

    with tempfile.NamedTemporaryFile() as scrapy_process_temp_file:
        # Scrapy configuration, launched aith tempm file
        process = CrawlerProcess(settings={
            "FEEDS": {
                '{}'.format(scrapy_process_temp_file.name): {
                    'format': 'json',
                    'encoding': 'utf8',
                    'indent': 4,
                },
            },
            "LOG_LEVEL":log_level,
            "DOWNLOAD_DELAY":3,
            "COOKIES_ENABLED":False,
            "SPIDER_MODULES":"alt_job.scrapers",
            "ITEM_PIPELINES": {
                'alt_job.pipelines.AddKeywordMatchesPipeline': 100
            },
            'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
            },
            'FAKEUSERAGENT_FALLBACK':'Mozilla'
        })

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

    
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # Mandatory Fields
    title = scrapy.Field()
    url = scrapy.Field()

    # extra fields that scrapers can fill
    organisation = scrapy.Field()
    date_posted = scrapy.Field()
    apply_before = scrapy.Field()
    location = scrapy.Field()
    job_type = scrapy.Field()
    salary = scrapy.Field()
    week_hours = scrapy.Field()
    description = scrapy.Field()

    # Fields filled by pipeline
    keywords_matched = scrapy.Field()
    source = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in Job.fields:
            self.setdefault(key, None)
        
    def get_text(self):
        return """Title: {title}

Organisation: {organisation}

Date posted: {date_posted}

Apply before: {apply_before}

URL: {url}

Location: {location}

Job type: {job_type}

Keywords matched: {keywords_matched}

Source: {source}

Description: {description}
""".format(**dict(self))

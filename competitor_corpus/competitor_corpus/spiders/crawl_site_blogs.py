#import libraries
import scrapy
from scrapy import signals
from urllib.parse import urljoin, urlparse
import urllib.parse
import os
import json
from datetime import datetime
import logging

from competitor_corpus.functions.parse_blogs import ParseBlogs

#scrapy crawl CrawlSiteBlogs
class CrawlSiteBlogs(scrapy.Spider):
    name = "CrawlSiteBlogs"

    def __init__(self):
        self.file_path = './2_output_files/1_sitemap_corpus'
        self.file_name = 'competitor_corpus'
        self.parseblogs = ParseBlogs()
        with open(f'{self.file_path}/{self.file_name}.json', 'r') as file:
            self.corpus_data = json.load(file)

        logging.info("Loaded start file")
        
        self.final_object = {}
        self.data_list = []
        self.error_list = []

    def start_requests(self):
        logging.info("Running start requests")
        
        for company, details in self.corpus_data.items():
            for page in details['all_pages']:
                if page.get('page_section') == 'blog':
                    page_link = page['page_link']
                    yield scrapy.Request(
                        url=page_link,
                        callback=self.parse_blog_page,
                        cb_kwargs={'current_page': page}
                    )

    def parse_blog_page(self, response, current_page):
        logging.info(f'Running parse_sitemap, this is the response: {response.status}')

        page = current_page
        company = current_page['company_name']
        page['page_published_date'] = self.parseblogs.grab_blog_date(company,response)

        # Update the original data_list in memory
        for company, details in self.corpus_data.items():
            for idx, p in enumerate(details['all_pages']):
                if p['page_link'] == current_page['page_link']:
                    self.corpus_data[company]['all_pages'][idx] = current_page
                    break

        with open(f'{self.file_path}/{self.file_name}.json', 'w') as file:
            json.dump(self.corpus_data, file, indent=2)


########################## Closing Functions ##########################################
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSiteBlogs, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        logging.info("CAUTION: The Spider Has Closed")

        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)
        logging.info("CAUTION: Now we're running the closing funtion")

        #Save self.data_list to a JSON file
        # with open('2_output_files/1_sitemap_corpus/competitor_corpus2.json', 'w') as f:
        #     json.dump(self.final_object, f, indent=2)



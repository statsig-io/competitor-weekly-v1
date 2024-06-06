#import libraries
import scrapy
from scrapy import signals
from urllib.parse import urljoin, urlparse
import urllib.parse
import os
import json
from datetime import datetime
import logging


#import helper functions
from competitor_corpus.functions.helper_functions import PrepData


#scrapy crawl CrawlSitemap
class CrawlSitemap(scrapy.Spider):
    name = "CrawlSitemap"

    def __init__(self):
        logging.info(f'Getting files {os.getcwd()}')

        self.file_path = './1_input_files'
        self.file_name = 'competitor_sitemaps'
        with open(f'{self.file_path}/{self.file_name}.json') as f:
            self.data = json.load(f)


        with open(f'{self.file_path}/competitor_corpus_temp.json') as f:
            self.data_template = json.load(f)

        logging.info("Loaded start file")
        self.prepdata = PrepData()
        self.final_object = {}
        self.data_list = []
        self.error_list = []


    def start_requests(self):
        logging.info("Running start requests")
        for competitor in self.data['competitors']:
            sitemap_url = competitor['company_sitemap']
        
            yield scrapy.Request(
                sitemap_url,
                callback=self.parse_sitemap,
                cb_kwargs={'current_run':competitor}
                )


    def parse_sitemap(self, response, current_run):
        logging.info(f'Running parse_sitemap, this is the response: {response.status}')
        
        current_competitor = current_run
        competitor_name = current_competitor['company_name']
        data_dict = self.data_template
        logging.info(f"Running this competitor: {competitor_name}")

        namespaces = {
            'sm': "http://www.sitemaps.org/schemas/sitemap/0.9",
            'xhtml': "http://www.w3.org/1999/xhtml"
        }

        for url in response.xpath('//sm:url', namespaces=namespaces):
            loc = url.xpath('sm:loc/text()', namespaces=namespaces).get().strip()
            changefreq = url.xpath('sm:changefreq/text()', namespaces=namespaces).get()
            priority = url.xpath('sm:priority/text()', namespaces=namespaces).get()
            
            data_dict['page_link'] = loc
            if "/blog" in loc:
                data_dict['page_section'] = 'blog'
            elif '/changelog' in loc or '/udpates.' in loc:
                data_dict['page_section'] = 'updates'

            data_dict['date_of_last_run'] = datetime.now().strftime('%Y-%m-%d')

            final_dict = {**current_competitor, **data_dict}
            self.data_list.append(final_dict.copy())

        #add page for Eppo's subdomain for updates
        if competitor_name == 'Eppo':
            data_dict['page_link'] = "https://updates.eppo.cloud/loadMoreNews?app_id=qZPczwWF46534&language=EN&user_id=f76eb8c9-bb3a-4a17-a566-5c40ab533ae1&publicPage=true&post=false&basePath=%2F%2Fupdates.eppo.cloud%2Fen&standaloneLogoUrl=https%3A%2F%2Fstatic.getbeamer.com%2FqZPczwWF46534%2Flogo_10694.png"
            data_dict['page_section'] = 'updates'
            data_dict['date_of_last_run'] = datetime.now().strftime('%Y-%m-%d')

            final_dict = {**current_competitor, **data_dict}
            self.data_list.append(final_dict.copy())
        
        self.final_object[competitor_name] = self.data_list
        self.data_list = []


########################## Closing Functions ##########################################
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrawlSitemap, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        logging.info("CAUTION: The Spider Has Closed")

        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)
        logging.info("CAUTION: Now we're running the closing funtion")

        #Save self.data_list to a JSON file
        with open('2_output_files/1_sitemap_corpus/competitor_corpus.json', 'w') as f:
            json.dump(self.final_object, f, indent=2)

    


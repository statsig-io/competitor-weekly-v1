from run_airops import RunAirops
from run_scraper import RunScraper
import json
import requests
import asyncio

class MainRun:
    def __init__(self) -> None:
        # to be replaced, currently just a list of updates pages
        with open('./1_input_files/competitor_corpus.json', 'r') as file:
            self.competitor_corpus = json.load(file)
        
        self.webhook_url = "https://hooks.zapier.com/hooks/catch/18994682/2o3slwl/"

    async def start(self):
        scraper = RunScraper(self.competitor_corpus)
        scraper_updates_corpus = await scraper.scrape_updates_page()
        scraper_updates_corpus_json = json.dumps(scraper_updates_corpus)
        # print('scraper_updates_corpus_json', scraper_updates_corpus)

        airops_response = await RunAirops().llm_model(scraper_updates_corpus_json)
        print('ran airops_response')

# python3 main.py
if __name__ == "__main__":
    main_run = MainRun()
    asyncio.run(main_run.start())


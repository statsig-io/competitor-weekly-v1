import json
from datetime import datetime
import asyncio
import aiohttp
from aiohttp import ClientResponse, ClientSession
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError
from requests import Response
from cred import *
from parse_updates_page import CompetitorParser
from proxie_request import MakeRequest

class RunScraper:
    def __init__(self, corpus_data) -> None:
        self.make_request = MakeRequest()
        self.corpus_data = corpus_data
        self.final_object = {company: [] for company in corpus_data.keys()}

    async def scrape_updates_page(self):
        tasks = []
        for company, item_ in self.corpus_data.items():
            tasks.append(self.process_company_updates(company, item_["current_updates_page"]))
        
        await asyncio.gather(*tasks)
        self.save_updates_corpus()
        return self.final_object

    async def process_company_updates(self, company, page_link):
        print(f'Running this competitor: {company}')
        print(f'Running this update page: {page_link}')

        try:
            response_status, response_contnet = await self.make_request.proxie_request(page_link)
            print(f'This is the response: {response_status}')                            
            if response_status == 200:
                if company == 'PostHog':
                    data_list = CompetitorParser().posthog_parse_page(response_contnet)
                elif company == 'Eppo':
                    data_list = CompetitorParser().eppo_parse_page(response_contnet)
                
                if len(data_list) >= 5:
                    data_list = data_list[:4]
                
                self.final_object[company].extend(data_list)
            else:
                print(f"Failed in Process Company: Failed to retrieve the page. Status code: {response_status}")

        except ClientConnectionError as e:
            print(f"Failed in Process Company: Connection error for {company}. Error: {e}")
        except ServerTimeoutError as e:
            print(f"Failed in Process Company: Server timeout for {company}. Error: {e}")
        except Exception as e:
            print(f"Failed in Process Company: Failed to retrieve the page for {company}. No Response. Error: {e}")

    def save_updates_corpus(self):
        with open('2_output_files/competitor_updates_corpus.json', 'w') as f:
            json.dump(self.final_object, f, indent=2)

# python3 run_scraper.py
if __name__ == "__main__":
    with open('./1_input_files/competitor_corpus.json', 'r') as file:
        corpus_data = json.load(file)

    run = RunScraper(corpus_data)
    asyncio.run(run.scrape_updates_page())



#######################################################################################################################################s


# import json
# from datetime import datetime

# #import files
# from cred import *
# from parse_updates_page import CompetitorParser
# from proxie_request import MakeRequest

# #python3 main.py
# class RunScraper:
#     def __init__(self, corpus_data) -> None:
#         self.make_request = MakeRequest()
#         self.corpus_data =corpus_data
        
#         self.data_list = []
#         self.final_object = {}
    

#     def scrape_updates_page(self):
#         for company, updaets_page, in self.corpus_data.items():
#             self.data_list = []
#             print('Running this competitor', company)
#             page_link = updaets_page
#             print('Running this update page', page_link)

#             response = self.make_request.proxie_request(page_link)
#             if response.status_code == 200:
#                 if company == 'PostHog':
#                     data_list = CompetitorParser().posthog_parse_page(response.content)

#                 elif company == 'Eppo':
#                     data_list = CompetitorParser().eppo_parse_page(response.content)
                    

#                 self.data_list.extend(data_list)
#                 len_of_list = len_of_list = len(self.data_list) if self.data_list else 0
#                 if len_of_list >= 5:
#                     self.data_list = self.data_list[:4]
                
#                 # self.final_object[company] = {'count_of_update': len_of_list, 'list_of_updates': self.data_list}
#                 self.final_object[company] = self.data_list

#             else:
#                 print(f"Failed to retrieve the page. Status code: {response.status_code}")

#         save_file  = self.save_udpates_corpus()


#     def save_udpates_corpus(self):
#         with open('2_output_files/competitor_updates_corpus.json', 'w') as f:
#             json.dump(self.final_object, f, indent=2)
        

# #python3 run_scraper.py
# if __name__ == "__main__":
#     with open('./1_input_files/competitor_corpus.json', 'r') as file:
#         corpus_data = json.load(file)

#     run = RunScraper().scrape_updates_page(corpus_data)

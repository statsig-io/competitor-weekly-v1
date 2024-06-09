import aiohttp
import asyncio
import json
from time import time, strftime, localtime
from cred import *

class RunAirops:
   def __init__(self) -> None:
      self.headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {airops_api}'
      }

   async def llm_model(self, updates_corpus):
      start_time = time()
      print("Start time:", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))

      llm_model_url = "https://api.airops.com/public_api/airops_apps/45c5b56d-02ad-4a43-8dfd-3e72a960fed3/async_execute"
      data = {
          "inputs": {
              "competitor_updates": updates_corpus
          }
      }

      try:
          async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
              async with session.post(llm_model_url, headers=self.headers, json=data) as response:
                  response_code = response.status
                  if response_code != 200:
                      raise Exception(f"Received unexpected status code {response_code}")
                  
                  print('Making request - here is the response', response_code)
                  response_data = await response.json()
      
      except aiohttp.ClientError as e:
          print("There was an error at RunAirops, function llm_model: ", e)
          response_data = None

      end_time = time()
      print("End time:", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))
      print("Duration:", end_time - start_time, "seconds")

      return response_data

# python3 run_airops.py
if __name__ == "__main__":
    async def main():
        # Load the JSON file
        with open('./2_output_files/test-updates.json', 'r') as file:
            corpus_data = json.load(file)

        response = await RunAirops().llm_model(corpus_data)

        if response:
            print("Response data:", response)
        else:
            print("Failed to get a valid response.")
    
    asyncio.run(main())














#######################################################################################################################################

# import requests
# import json
# from time import time, strftime, localtime

# from cred import *

# class RunAirops:
#    def __init__(self) -> None:
#       self.headers = {
#           'Content-Type': 'application/json',
#           'Authorization': f'Bearer {airops_api}'
#       }

#    def llm_model(self, updates_corpus):
#       start_time = time()
#       print("Start time:", strftime('%Y-%m-%d %H:%M:%S', localtime(start_time)))

#       llm_model = "https://app.airops.com/public_api/airops_apps/45c5b56d-02ad-4a43-8dfd-3e72a960fed3/execute"
#       data = {
#           "inputs": {
#               "competitor_updates": updates_corpus
#           }
#       }

#       try:
#         response = requests.post(llm_model, headers=self.headers, json=data)
#         response_code = response.status_code

#         if response_code != 200:
#           raise Exception(f"Received unexpected status code {response_code}")
        
#         print('Making request - here is the response', response_code)
#         response_data = response.json()
      
#       except requests as e:
#         print("There was an error at RunAirops, function llm_model: ", e)
#         response_data = None

#       end_time = time()
#       print("End time:", strftime('%Y-%m-%d %H:%M:%S', localtime(end_time)))
#       print("Duration:", end_time - start_time, "seconds")

#       return response_data


#python3 airops_auth.py
# if __name__ == "__main__":

#   # Load the JSON file
#   with open('./2_output_files/test-updates.json', 'r') as file:
#       corpus_data = json.load(file)

#   response = RunAirops().llm_model(corpus_data)

#   if response:
#       print("Response data:", response)
#   else:
#       print("Failed to get a valid response.")



  
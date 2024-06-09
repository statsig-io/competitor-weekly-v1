import aiohttp
import asyncio
import ssl
from aiohttp import BasicAuth
from aiohttp.client_exceptions import ClientConnectionError
import requests

class MakeRequest:
    def __init__(self) -> None:
        pass
    
    async def proxie_request(self, url, retries=3):
        ssl_context = ssl.create_default_context(cafile='./zyte-smartproxy-ca.crt')
        proxy_url = "http://proxy.crawlera.com:8011/"
        proxy_auth = BasicAuth('5d10d14c510e467ca77276d827957591', '')

        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                    async with session.get(
                        url,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth,
                        ssl=ssl_context
                    ) as response:
                        print(
                            f"Requesting [{url}]\n\n"
                            f"Response Code: {response.status}\n"
                            f"Response Headers: {response.headers}\n"
                        )
                        if response.status == 200:
                            content = await response.text()
                            print("Response Content:", content[:200])  # Print the first 200 characters of the response content
                            return response
                        else:
                            print(f"Failed to retrieve the page. Status code: {response.status}")
                            if response.status >= 500:
                                raise ClientConnectionError
            except ClientConnectionError as e:
                print(f"ClientConnectionError: {e}")
                if attempt < retries - 1:
                    print("Retrying...")
                    await asyncio.sleep(2)
                else:
                    print("Failed after retries. Switching to synchronous request.")
                    return self.sync_proxie_request(url)
            except Exception as e:
                print(f"An error occurred: {e}")
                if attempt == retries - 1:
                    print("Switching to synchronous request.")
                    return self.sync_proxie_request(url)

    def sync_proxie_request(self, url):
        try:
            response = requests.get(
                url,
                proxies={
                    "http": "http://5d10d14c510e467ca77276d827957591:@proxy.crawlera.com:8011/",
                    "https": "http://5d10d14c510e467ca77276d827957591:@proxy.crawlera.com:8011/",
                },
                verify='./zyte-smartproxy-ca.crt' 
            )
            print(
                f"Requesting [{url}]\n\n"
                f"Response Time: {response.elapsed.total_seconds()}\n"
                f"Response Code: {response.status_code}\n"
                f"Response Headers: {response.headers}\n"
            )
            return response
        except Exception as e:
            print(f"An error occurred during synchronous request: {e}")
            return None


#python3 proxie_request.py
if __name__ == "__main__":
    async def main():
        url = "https://updates.eppo.cloud/loadMoreNews?app_id=qZPczwWF46534&language=EN&user_id=f76eb8c9-bb3a-4a17-a566-5c40ab533ae1&publicPage=true&post=false&basePath=%2F%2Fupdates.eppo.cloud%2Fen&standaloneLogoUrl=https%3A%2F%2Fstatic.getbeamer.com%2FqZPczwWF46534%2Flogo_10694.png"  # Replace with the URL you want to test
        make_request = MakeRequest()
        response = await make_request.proxie_request(url)
        
    asyncio.run(main())


#######################################################################################################################################s

# import requests

# class MakeRequest:
#     def __init__(self) -> None:
#           pass
    
#     def proxie_request(self, url):
#             response = requests.get(
#                 url,
#                 proxies={
#                     "http": "http://5d10d14c510e467ca77276d827957591:@proxy.crawlera.com:8011/",
#                     "https": "http://5d10d14c510e467ca77276d827957591:@proxy.crawlera.com:8011/",
#                 },
#                 verify='./zyte-smartproxy-ca.crt' 
#             )

#             # print(
#             #     f"Requesting [{url}]\n\n"
#             #     "Request Headers:"
#             #     f"{response.request.headers}\n"
#             #     f"Response Time: {response.elapsed.total_seconds()}\n"
#             #     f"Response Code: {response.status_code}\n"
#             #     f"Response Headers: {response.headers}\n"
#             # )

#             print(
#                 f"Requesting [{url}]\n\n"
#                 f"Response Time: {response.elapsed.total_seconds()}\n"
#                 f"Response Code: {response.status_code}\n"
#             )

#             return response
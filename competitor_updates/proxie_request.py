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
                            # print("Response Content:", content[:200])
                            return response.status, content
                        
                        else:
                            print(f"Failed in Proxie Request: Failed to retrieve the page. Status code: {response.status}")
                            if response.status >= 500:
                                raise ClientConnectionError
            
            except ClientConnectionError as e:
                print(f"ClientConnectionError: {e}")
                if attempt < retries - 1:
                    print("Retrying...")
                    await asyncio.sleep(2)
                else:
                    print("Failed in Proxie Request: Failed after retries. Switching to synchronous request.")
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
            return response.status_code, response.content
        except Exception as e:
            print(f"An error occurred during synchronous request: {e}")
            return None, None


#python3 proxie_request.py
if __name__ == "__main__":
    async def main():
        url = "https://posthog.com/changelog/2024"  # Replace with the URL you want to test
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
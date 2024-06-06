from urllib.parse import urljoin
import urllib.parse
import datetime
from datetime import datetime 
import traceback


class PrepData:
    def __init__(self) -> None:
        pass

    def get_domain(self, url):
        domain = None
        try:
            parsed_url = urllib.parse.urlparse(url)
            domain = parsed_url.netloc

            if 'www.' in domain:
                domain = domain.split('www.')[-1]
            
        except Exception as e:
            print(f"Error processing the URL: {e}")
        
        return domain
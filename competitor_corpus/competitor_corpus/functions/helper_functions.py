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
    


# #python3 functions/helper_functions.py
# import json

# def get_blog_sections(file_path):
#     # Load the JSON data from the file
#     with open(file_path, 'r') as file:
#         data = json.load(file)

#     # Initialize a list to store the filtered objects
#     blog_sections = []

#     # Iterate through the data and filter the objects
#     for company, pages in data.items():
#         for page in pages:
#             if page.get('page_section') == 'blog':
#                 blog_sections.append(page)
    
#     return blog_sections




# # File path to the competitor_corpus.json file
# file_path = './2_output_files/1_sitemap_corpus/competitor_corpus.json'

# # Get the list of blog sections
# blog_sections = get_blog_sections(file_path)

# # Print the result
# print(json.dumps(blog_sections, indent=2))
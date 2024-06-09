from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

#import files
from cred import *

class CompetitorParser:
    def __init__(self) -> None:
        self.data_list = []


    def posthog_parse_page(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        section = soup.find('section', class_='grid article-content')

        if section:
            divs = section.find_all('div', class_='flex gap-4')
            for div in divs:
                # Find month and year section titles
                section_date_month = div.find('h2', class_='!text-sm font-bold uppercase !m-0')
                section_date_year = div.find('div', class_='text-xs font-semibold')

                month = section_date_month.get_text(strip=True) if section_date_month else "Unknown Month"
                year = section_date_year.get_text(strip=True) if section_date_year else "Unknown Year"
                section_date = f"{month} {year}"

                ul = div.find('ul', class_='list-none m-0 p-0 grid gap-y-12 flex-1 pb-12')
                if ul:
                    lis = ul.find_all('li')
                    for li in lis:
                        update = {}
                        update['update_period'] = section_date
                        relative_div = li.find('div', class_='relative')
                        if relative_div:
                            # Extract update title and category
                            h3 = relative_div.find('h3')
                            if h3:
                                update['update_title'] = h3.get_text(strip=True)
                            p = relative_div.find('p')
                            if p:
                                update['update_category'] = p.get_text(strip=True)
                            
                            # Extract span text
                            span = relative_div.find('span')
                            if span:
                                update['update_span_text'] = span.get_text(strip=True)
                            
                            # Extract update text from the div with class "mt-2"
                            mt2_div = li.find('div', class_='mt-2')
                            if mt2_div:
                                update['update_text'] = mt2_div.get_text(strip=True)

                            update['date_of_last_run'] = datetime.now().strftime('%Y-%m-%d')
                            
                            self.data_list.append(update.copy())
            
            # len_of_list = len(data_list) if data_list else None

        else:
            print("No section with class 'grid article-content' found")

        return self.data_list
    

    def eppo_parse_page(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        update = {}

        # Find all <div> elements with the attribute role="listitem" using CSS selectors
        listitem_divs = soup.select('div[role="listitem"]')
        
        # Process each <div> element
        for div_item in listitem_divs:
            section_date = div_item.find('div', class_='featureDate').find('span')
            
            if section_date:
                date_text = section_date.get_text(strip=True)
                date_obj = datetime.strptime(date_text, "%B %d, %Y")
                formatted_date = date_obj.strftime("%b %Y")

                update['update_period'] = formatted_date
                # print(f"Formatted Date: {formatted_date}")

            section_title = div_item.get('data-post-title')
            update['update_title'] = section_title
            # print(f"Section Title: {section_title}")

            update['update_category'] = ""

            update['update_span_text'] = ""
            # print(f"Section Sub Text: {section_title}")

            section_text = div_item.find('div', class_ = 'featureContent').get_text(strip=True)
            update['update_text'] = section_text
            # print(f"Section Text: {section_text}")

            self.data_list.append(update.copy())
        
        return self.data_list
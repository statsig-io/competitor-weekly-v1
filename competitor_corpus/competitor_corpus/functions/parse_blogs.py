from dateutil import parser
import json


class ParseBlogs:
    def __init__(self) -> None:
        pass

    def grab_blog_date(self, competitor, response):
        print("Grabbing blog page")
        print("This is the competitor", competitor)

        page_date = None

        if competitor == 'PostHog':
            page_date = response.xpath('//p[@class="mb-1 opacity-70"]/text()').get().strip() if response.xpath('//p[@class="mb-1 opacity-70"]').get() else ''
        
        elif competitor == 'Eppo':
            page_date = response.xpath('//div[@class="text--regular"]/text()').get().strip() if response.xpath('//div[@class="text--regular"]').get() else ''

        elif competitor == 'LaunchDarkly':
            page_date = response.xpath('//div[@class="styles-module--timestamp--c580a"]/text()').get().strip() if response.xpath('//div[@class="styles-module--timestamp--c580a"]').get() else ''

        if page_date != None:
            page_date = self.convert_to_datetime(page_date)

        return page_date
            

    def convert_to_datetime(self, date_text):
        # Parse the date string and convert to datetime object
        try:
            date_obj = parser.parse(date_text)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Error parsing date: {date_text}")
            return None


#python3 functions/parse_blogs.py
# print(ParseBlogs().convert_to_datetime('May 31, 2024'))
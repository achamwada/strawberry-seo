import requests
from bs4 import BeautifulSoup
import tldextract as urlData
import re
from datetime import date


class Pulp:

    def __init__(self, url):

        self.url = url
        self.url_object = urlData.extract(url)
        self.site_name = self.url_object.domain

    def create_site_map(self):
        ### Function to generate a site map on crawled urls ###
        print("Creating xml...")

        req = requests.get(self.url)

        soup = BeautifulSoup(req.content, 'html.parser')

        all_links = soup.find_all('a')
        site_map = []

        for link in all_links:

            # Check if its a relative link
            if self.url not in link['href'] and '#' not in link['href']:

                link['href'] = "{}/{}".format(str(self.url).rstrip("/"),link['href'])

            if self.url in link['href'] and link['href']:

                site_map.append(link['href'])

                if self.url in link['href']:

                    more_content = requests.get(link['href'])
                    more_soup = BeautifulSoup(more_content.content, 'html.parser')
                    more_links = more_soup.find_all('a')

                    for mlinks in more_links:

                        try:
                            if self.url in mlinks['href'] :
                                site_map.append(mlinks['href'])

                        except Exception as e:
                            print(str(e))

        # cleaning
        clean_links = []
        for m in site_map:

            if "http" in m and "#" not in m and m not in clean_links:
                clean_links.append(m)

        start_str = '<?xml version="1.0" encoding="UTF-8"?>\r<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\r'
        end_str = '\r</urlset>'

        today = date.today()

        # Unix file system / but windows \
        f = open("sitemaps/{}_sitemap.xml".format(str(self.site_name)), mode="w")

        f.write(start_str)
        i = 1

        for each_url in clean_links:

            priority = self.calculate_priority(each_url)

            if priority > 0.8:
                changefreq = 'weekly'

            elif priority > 0.5 and priority <= 0.8:
                changefreq = 'monthly'

            else:
                changefreq = 'yearly'

            # Site map url object
            f.write("""
            <url>
              <loc>{}</loc>
              <lastmod>{}</lastmod>
              <changefreq>{}</changefreq>
              <priority>{}</priority>
            </url>""".format(str(each_url), str(today), changefreq, priority))

            i = i + 1
        f.write(end_str)

        f.close()

    @staticmethod
    def calculate_priority(search_url):
        ### Function to determine page priority based on its distance from the domain ###

        url_list = re.sub(r'https://|http://|//+', '', search_url).rstrip("/").split("/")
        bench_mark = 10

        current_url_limit = len(url_list)

        if current_url_limit >= bench_mark:
            return 0.1

        return round((1 - float(current_url_limit / bench_mark)), 2)

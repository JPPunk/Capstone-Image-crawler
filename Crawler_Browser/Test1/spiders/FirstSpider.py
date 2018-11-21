""" The code is part of Phishing Detection Through Image Analysis
Capstone Project conducted under supervision of DR SURANGA.

Author: Kunjan Patel, Jipeng Lu and Gavin Borges

Purpose: The main purpose of this part of code is to run a headless web
browser in background and capture screenshot of crawled URLs. """
import csv
import scrapy
from Test1.items import FirstSpiderItem
import logging
# Create the logging file of Scrapy
logging.basicConfig(filename='logging01.log', level=logging.DEBUG)


# Define the first spider
class MySpider1(scrapy.Spider):
    name = 'firstspider'
    # Define start URLs and the domain names which the spiders should follow
    allowed_domains = []
    start_urls = []
    
    # import domain names and start URLs from input csv file.
    with open("input.csv", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            allowed_domains.append(row[0])
            start_urls.append(row[1])
        print(allowed_domains)
        print(start_urls)

    # Parse the HTML of the web page and extract links from this site.
    def parse(self, response):
        sel = scrapy.Selector(response)
        links_in_one_page = sel.xpath('//a[@href]')

        for link_sel in links_in_one_page:
            item = FirstSpiderItem()
            link = str(link_sel.re('href="(.*?)"')[0])
            if link:
                if not link.startswith('http'):
                    link = response.url + link
                yield scrapy.Request(link, callback=self.parse)

                item['link'] = link
                yield item


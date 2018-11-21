#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" The code is part of Phishing Detection Through Image Analysis
Capstone Project conducted under supervision of DR SURANGA.

Author: Kunjan Patel, Jipeng Lu and Gavin Borges

Purpose: The main purpose of this part of code is to run a headless web
browser in background and capture screenshot of crawled URLs. """

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
import csv


class FirstSpiderPipeline(object):

    def __init__(self):
        #Create a csv file to save the links we got.
        self.file = open('draft.csv', 'w')
        self.seen = set()
    #Drop the duplicated links and put them into fields
    def process_item(self, item, spider):
        if item['link'] in self.seen:
            raise DropItem('Duplicate link %s' % item['link'])
        self.seen.add(item['link'])

        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item


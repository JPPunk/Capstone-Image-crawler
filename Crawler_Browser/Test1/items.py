#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" The code is part of Phishing Detection Through Image Analysis
Capstone Project conducted under supervision of DR SURANGA.

Author: Kunjan Patel, Jipeng Lu and Gavin Borges

Purpose: The main purpose of this part of code is to run a headless web
browser in background and capture screenshot of crawled URLs. """

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    link = scrapy.Field()


""" The code is part of Phishing Detection Through Image Analysis
Capstone Project conducted under supervision of DR SURANGA.

Author: Kunjan Patel, Jipeng Lu and Gavin Borges

Purpose: The main purpose of this part of code is to run a headless web
browser in background and capture screenshot of crawled URLs. """

import glob
import io
import os
import sqlite3
import time
import multiprocessing
from Crypto.Hash import MD2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Establish database connection
DatabaseConnect = sqlite3.connect('Database01.db')

# Create cursor that executes various queries in database
ExecuteQuery = DatabaseConnect.cursor()


# This function fetches record from the database
def FetchRecord():
    # print("Fetching Record from  Database")

    # Fetches distinct record from database
    FetchRecord = '''select distinct * from "Test" where flag=0 or flag1=0 order by random() limit 1'''

    # Executes FecthRecord query
    ExecuteQuery.execute(FetchRecord)

    # Loop extracts different URL, FLAG and Domain from row array
    for row in ExecuteQuery:
        # print(row)

        # if firstflag is zero then return URL and Domain
        if row[2] == 0:
            # print("Fetched Record is ", row[0])
            return row[1], row[0]
        else:
            print("Seems No URL Left in Database")


# First headless browser instance
def HeadlessBrowserInstance1():
    start = time.time()

    # Record variable with empty array
    Record = []

    # calling FetchRecord and storing return values i.e. URL and DOMAIN in Record[]
    Record = FetchRecord()
    url = Record[0]
    domain = Record[1]

    flag1 = int(1)
    try:
        # Updating FLAG1 in database for specific URL so another browser instance works on different URL
        updateflag1 = '''update Test set FLAG1=? where URL=?'''
        ExecuteQuery.execute(updateflag1, (flag1, url))
        DatabaseConnect.commit()
    except Exception as e:
        print(e)

    # storing arguments of headless browser in by importing Options
    parameters = Options()

    # --headless forces browser instance to work in headless mode
    parameters.add_argument("--headless")

    # creating webdriver variable for firefox by passing parameters and adding Gecko web driver to call firefox via python
    browser = webdriver.Firefox(firefox_options=parameters, executable_path=r'C:\\webdriver\\geckodriver')

    # maximizing window of headless firefox
    browser.maximize_window()

    try:
        # Passing URL in headlesss firefox
        browser.get(url)
    except Exception as e:
        print(e)

    # generating Unique MD2 hash of each URL and convert them into string
    starthashtime = time.time()
    hashurl = str.encode(url)
    SHAVALUE = MD2.new(hashurl)
    endhashtime = time.time()

    # Capturing screenshot of webpage as PNG
    capturescreen = browser.get_screenshot_as_png()

    # quality is a parameter used while converting png to jpeg
    quality = 100

    # converting PNG into Bytes and then into jpeg
    try:
        img = Image.open(io.BytesIO(capturescreen))
        img = img.convert("RGB")
    except Exception as e:
        print(e)

    # creating subfolders with domain as naming convention under ScreenShots folder
    try:
        os.makedirs(os.path.join(r".\\ScreenShots\\", str(domain)))
    except Exception as e:
        print(e)

    # FolderPath stores path for that particular domain
    FolderPath = os.path.join(r'.\\ScreenShots\\', str(domain) + '\\')

    # Glob loop to scan all the domain directories in ScreenShots folder
    for folders in glob.glob(r'.\\ScreenShots\\*'):

        # If domain folder exists store converted screenshot of that URL in that specific domain
        if os.path.exists(FolderPath):
            StoragePath = os.path.join(r'.\\ScreenShots', str(domain) + '\\')

            # saving Image by specifying quality and setting image optimization to true
            try:
                img.save(str(StoragePath) + str(SHAVALUE.hexdigest()) + '.jpeg', 'JPEG', quality=quality,
                         optimise=True)
            except Exception as e:
                print(e)

        #  If domain folder doesn't exist create new folder and store image
        else:
            os.makedirs(os.path.join(r".\\ScreenShots\\", str(domain)))

            StoragePath = os.path.join(r'.\\ScreenShots', str(domain) + '\\')

            try:
                img.save(str(StoragePath) + str(SHAVALUE.hexdigest()) + '.jpeg', 'JPEG', quality=quality,
                         optimise=True)
            except Exception as e:
                print(e)

    # Converting hash into string, flag into integer, path into string
    hash = str(SHAVALUE.hexdigest())
    flag = int(1)
    Location = str(StoragePath) + hash + '.jpeg'
    Location = Location.strip(".\\")

    # updating record in database by updating flags, hash and path of that image
    try:
        updateHASH = ('''UPDATE "Test" SET FLAG=?, HASH=?, PATH=? WHERE URL = ?''')
        ExecuteQuery.execute(updateHASH, (flag, hash, Location, url))
        DatabaseConnect.commit()
    except Exception as e:
        print(e)

    # Safely closing browser instance
    browser.close()
    browser.quit()

    end = time.time()

#Second headless browser instance
def HeadlessBrowserInstance2():
    start = time.time()

    # Record variable with empty array
    Record = []

    # calling FetchRecord and storing return values i.e. URL and DOMAIN in Record[]
    Record = FetchRecord()
    url = Record[0]
    domain = Record[1]

    flag1 = int(1)
    try:
        # Updating FLAG1 in database for specific URL so another browser instance works on different URL
        updateflag1 = '''update Test set FLAG1=? where URL=?'''
        ExecuteQuery.execute(updateflag1, (flag1, url))
        DatabaseConnect.commit()
    except Exception as e:
        print(e)

    # storing arguments of headless browser in by importing Options
    parameters = Options()

    # --headless forces browser instance to work in headless mode
    parameters.add_argument("--headless")

    # creating webdriver variable for firefox by passing parameters and adding Gecko web driver to call firefox via python
    browser = webdriver.Firefox(firefox_options=parameters, executable_path=r'C:\\webdriver\\geckodriver')

    # maximizing window of headless firefox
    browser.maximize_window()

    try:
        # Passing URL in headlesss firefox
        browser.get(url)
    except Exception as e:
        print(e)

    # generating Unique MD2 hash of each URL and convert them into string
    starthashtime = time.time()
    hashurl = str.encode(url)
    SHAVALUE = MD2.new(hashurl)
    endhashtime = time.time()

    # Capturing screenshot of webpage as PNG
    capturescreen = browser.get_screenshot_as_png()

    # quality is a parameter used while converting png to jpeg
    quality = 100

    # converting PNG into Bytes and then into jpeg
    try:
        img = Image.open(io.BytesIO(capturescreen))
        img = img.convert("RGB")
    except Exception as e:
        print(e)

    # creating subfolders with domain as naming convention under ScreenShots folder
    try:
        os.makedirs(os.path.join(r".\\ScreenShots\\", str(domain)))
    except Exception as e:
        print(e)

    # FolderPath stores path for that particular domain
    FolderPath = os.path.join(r'.\\ScreenShots\\', str(domain) + '\\')

    # Glob loop to scan all the domain directories in ScreenShots folder
    for folders in glob.glob(r'.\\ScreenShots\\*'):

        # If domain folder exists store converted screenshot of that URL in that specific domain
        if os.path.exists(FolderPath):
            StoragePath = os.path.join(r'.\\ScreenShots', str(domain) + '\\')

            # saving Image by specifying quality and setting image optimization to true
            try:
                img.save(str(StoragePath) + str(SHAVALUE.hexdigest()) + '.jpeg', 'JPEG', quality=quality,
                         optimise=True)
            except Exception as e:
                print(e)

        #  If domain folder doesn't exist create new folder and store image
        else:
            os.makedirs(os.path.join(r".\\ScreenShots\\", str(domain)))

            StoragePath = os.path.join(r'.\\ScreenShots', str(domain) + '\\')

            try:
                img.save(str(StoragePath) + str(SHAVALUE.hexdigest()) + '.jpeg', 'JPEG', quality=quality,
                         optimise=True)
            except Exception as e:
                print(e)

    # Converting hash into string, flag into integer, path into string
    hash = str(SHAVALUE.hexdigest())
    flag = int(1)
    Location = str(StoragePath) + hash + '.jpeg'
    Location = Location.strip(".\\")

    # updating record in database by updating flags, hash and path of that image
    try:
        updateHASH = ('''UPDATE "Test" SET FLAG=?, HASH=?, PATH=? WHERE URL = ?''')
        ExecuteQuery.execute(updateHASH, (flag, hash, Location, url))
        DatabaseConnect.commit()
    except Exception as e:
        print(e)

    # Safely closing browser instance
    browser.close()
    browser.quit()

    end = time.time()


# if __name__ == '__main__':
#     Scriptstart = time.time()
#     print(str(Scriptstart) + "seconds")
#     try:
#         while True:
#             # Creating browser Processes
#             BrowserProcess1 = multiprocessing.Process(target=HeadlessBrowserInstance1())
#             BrowserProcess2 = multiprocessing.Process(target=HeadlessBrowserInstance2())
# 
#             # Starting Processes
#             BrowserProcess1.start()
#             BrowserProcess2.start()
# 
#             # Closing Processes
#             BrowserProcess1.join()
#             BrowserProcess2.join()
#     except Exception as e:
#         print(e)
# 
#     Scriptend = time.time()
#     print(str(Scriptend) + "seconds")

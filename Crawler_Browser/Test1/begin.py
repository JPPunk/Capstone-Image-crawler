""" The code is part of Phishing Detection Through Image Analysis
Capstone Project conducted under supervision of DR SURANGA.

Author: Kunjan Patel, Jipeng Lu and Gavin Borges

Purpose: The main purpose of this part of code is to run a headless web
browser in background and capture screenshot of crawled URLs. """


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Test1.process_url import Edit
from Test1.BrowserInstance import *
import time

if __name__ == "__main__":
    #Start the spider and time keeping
    start = time.time()
    process = CrawlerProcess(get_project_settings())
    process.crawl('firstspider')
    process.start()
    #Launch process file to process URLs that spider crawled
    print("Editing...Please wait(Processes=4)")
    edit2 = Edit()
    edit2.editing()
    print("writing into databases...")
    edit2.multi(edit2.store)
    print("Successfully into databases!")
    
    # Launch the file which saves screen shots.
    try:
        while True:
            nondaemonThread1 = multiprocessing.Process(target=HeadlessBrowserInstance1())
            nondaemonThread1.start()
            nondaemonThread2 = multiprocessing.Process(target=HeadlessBrowserInstance2())
            nondaemonThread2.start()
            # nondaemonThread1.setDaemon(True)
            # nondaemonThread2.setDaemon(True)
            # nondaemonThread2.start()
            nondaemonThread1.join()
            nondaemonThread2.join()
    except Exception as e:
        print("Error occurred")
        print(e)
  
    end = time.time()
    print("Total Execution time is " + str(end - start) + "seconds")

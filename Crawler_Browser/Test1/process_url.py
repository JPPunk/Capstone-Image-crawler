#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Jasper
import csv, requests, sqlite3, multiprocessing


class Edit():
    domains = []
    cache0 = []
    transit = []
    buffer = []
    cache = []
    store = []
    outcome = []

    def __init__(self):
        pass
    #Create a new list with domains and URLs to save data.
    def editing(self):
        with open("input.csv", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.domains.append(row[0])

        with open("draft.csv", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.cache0.append(row[0])
            for c in self.cache0:
                c1 = c[10:-2]
                self.cache.append(c1)
    #Filter the URLs in levels by setting the number of '/'.  
        for dname in range(len(self.domains)):
            for ca in self.cache:
                if (self.domains[dname] in ca):
                    if ca.count('/') <= 7:
                        self.transit.append(ca)
                        self.cache.remove(ca)
                else:
                    continue
            self.buffer = self.transit[0:50]
            self.store.append(self.buffer)
            self.transit = []
            self.buffer = []
    #Filter the URLs by deleting some invalid pages with 40x error, and redirection of 30x status.
    def http_status(self, msg):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
            r = requests.get(msg, headers=headers, allow_redirects=False)
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                return msg
            elif r.status_code >= 300 and r.status_code <= 400:
                html = requests.get(msg, headers=headers, allow_redirects=False)
                url1 = html.headers['Location']
                if html.status_code < 300:
                    return url1
        except Exception as e:
            print(e)
    
    #Use multiprocess to detect each group of domains.
    #Create databases and import data into databases.
    def multi(self, urls):
        pool = multiprocessing.Pool(processes=4)
        results = []
        new = []
        conn = sqlite3.connect("Database01.db")
        curs = conn.cursor()
        for u in range(len(urls)):
            for ui in range(len(urls[u])):
                results.append(pool.apply_async(self.http_status, (urls[u][ui],)))
            for res in results:
                new.append(res.get())
            while None in new:
                new.remove(None)
            new = list(set(new))
            new.sort(key=lambda x: len(x))

            for i in range(len(new)):
                to_do1 = [self.domains[u], new[i]]
                print(new[i])
                curs.execute("INSERT INTO Test (DOMAIN,URL) VALUES (?, ?);", to_do1)
            new = []
            results = []
            conn.commit()

# if __name__ == "__main__":
#     print("Editing...Please wait(Processes=4)")
#     edit2 = Edit()
#     edit2.editing()
#     print("writing into databases...")
#     edit2.multi(edit2.store)
#     print("Successfully into databases!")

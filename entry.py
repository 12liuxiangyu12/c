# -*- coding:utf-8 -*-

import Crawler
from UrlPool import UrlPool
from bs4 import BeautifulSoup
import urlparse

class Entry(UrlPool):
    def __init__(self, seedUrl=[], max_depth=3, max_crawler=5):
        super(Entry, self).__init__(seedUrl=seedUrl, max_depth=max_depth)
        self.crawler_list = []
        for i in range(max_crawler):
            crawler = Crawler.Crawler(self, i)
            crawler.start()
            self.crawler_list.append(crawler)

    def complete(self):
        for crawler in self.crawler_list:
            crawler.stop()

    def handle_response(self, url, r):
        id = url[0]
        url = url[1]
        url = urlparse.urlparse(url)
        url = url.scheme + "://" + url.netloc
        content = r.content
        soup = BeautifulSoup(content)
        title = ""
        if soup.title:
            title = soup.title.string
        depth = self.db_method.get_depth_by_id(id)
        depth += 1
        self.db_method.update_url(id,
                            title=title)
        for link in soup.find_all('a'):
            href = link.get("href")
            if not href:
                continue
            if href.find("http") < 0:
                href = url + href
            if not self.db_method.is_url_exist(href):
                self.insert_url(href, depth)

if __name__ == "__main__":
    seedUrl = ["http://www.baidu.com","http://www.v2ex.com"]
    entry = Entry(seedUrl)

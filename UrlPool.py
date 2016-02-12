# -*- coding:utf-8 -*-

from time import sleep
import urlparse

from db_method import Db_Method

sleep_time = 60

class UrlPool(object):
    def __init__(self,seedUrl=[], max_depth=3):
        self.pool = []
        self.depth = 0
        self.is_loading = False
        self.db_method = Db_Method()
        self.max_depth = max_depth
        for url in seedUrl:
            self.insert_url(url, 0)
        self.get_url_by_depth(self.depth)

    def insert_url(self, url, depth):
        u = urlparse.urlparse(url)
        isHomePage = 0
        if not u.path and not u.query:
            isHomePage = 1
        self.db_method.insert_url(url=url,
                depth=depth,
                isHomePage=isHomePage)
        homepage = self.get_home_page_url(url)
        if not self.db_method.is_url_exist(homepage):
            self.insert_url(self.get_home_page_url(homepage), depth+1)

    def get_home_page_url(self, url):
        u = urlparse.urlparse(url)
        return u.scheme + "://" + u.netloc

    def get_url_by_depth(self, depth):
        urls = self.db_method.get_url_by_depth(depth)
        for url in urls:
            self.pool.append(url)

    def get_url_next_depth(self):
        if self.is_loading:
            return False
        if self.depth >= self.max_depth:
            if hasattr(self, "complete"):
                self.complete()
            return False
        self.is_loading = True
        sleep(sleep_time)
        self.depth += 1
        self.get_url_by_depth(self.depth)
        self.is_loading = False
        return self.pool and True or False

    def get_url(self):
        if self.pool:
            return self.pool.pop(0), self.depth
        elif self.get_url_next_depth():
            return self.pool.pop(0), self.depth
        else:
            return (None,None), None

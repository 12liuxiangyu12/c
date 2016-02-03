import Crawler
from UrlPool import UrlPool

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

if __name__ == "__main__":
    seedUrl = ["http://www.baidu.com","http://www.v2ex.com"]
    entry = Entry(seedUrl)

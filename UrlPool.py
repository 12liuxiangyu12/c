from db_method import Db_Method
class UrlPool(object):
    def __init__(self,seedUrl=[], max_depth=3):
        self.pool = []
        self.depth = 0
        self.db_method = Db_Method()
        self.max_depth = max_depth
        for url in seedUrl:
            self.insert_url(url, 0)
        self.get_url_by_depth(self.depth)

    def insert_url(self, url, depth):
        self.db_method.insert_url(url=url,
                depth=depth)

    def get_url_by_depth(self, depth):
        urls = self.db_method.get_url_by_depth(depth)
        for url in urls:
            self.pool.append(url)

    def get_url_next_depth(self):
        if self.depth >= self.max_depth:
            if hasattr(self, "complete"):
                self.complete()
            return False
        self.depth += 1
        self.get_url_by_depth(self.depth)
        return self.pool and True or False

    def get_url(self):
        if self.pool:
            print 'into 1'
            return self.pool.pop(0), self.depth
        elif self.get_url_next_depth():
            print 'into 2'
            return self.pool.pop(0), self.depth
        else:
            print 'into 3'
            return (None,None), None

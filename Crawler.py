# -*- coding:utf-8 -*-

import requests
import random
import threading
from time import ctime, sleep
LOOP_TIMEOUT = 3

class Crawler(threading.Thread):
    def __init__(self, pool, id):
        super(Crawler, self).__init__()
        print "init crawler " + str(id)
        self.isOpen = True
        self.id = str(id)
        self.pool = pool

    def openUrl(self, url):
        id = url[0]
        link = url[1]
        try:
            r = requests.get(link)
            if hasattr(self.pool, "handle_response"):
                self.pool.handle_response(url, r)
        except Exception, e:
            print e
            self.pool.db_method.update_url(id)
        finally:
            pass

    def stop(self):
        self.isOpen = False

    def run(self):
        while self.isOpen:
            url, depth = self.pool.get_url()
            if not url[1]:
                print 'waiting for url'
                sleep(LOOP_TIMEOUT)
                continue
            self.openUrl(url)
            sleep(2*(random.random()))
            print str(self.id) + " run:" + str(url[1]) + " depth:" +  str(depth)
        print "stop crawler " + str(self.id)

if __name__ == "__main__":
    pass

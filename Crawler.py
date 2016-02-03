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
        pass

    def stop(self):
        self.isOpen = False

    def run(self):
        while self.isOpen:
            url, depth = self.pool.get_url()
            if not url:
                print 'waiting for url'
                sleep(LOOP_TIMEOUT)
                continue
            sleep(2*(random.random()))
            print str(self.id) + " run:" + str(url[1]) + " depth:" +  str(depth)
        print "stop crawler " + str(self.id)

if __name__ == "__main__":
    pass

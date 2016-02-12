# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, create_engine, INTEGER, DATETIME, INTEGER, VARCHAR, TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import func
from sqlalchemy.orm import scoped_session
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

sql_url = "mysql://root:@localhost:3306/crawler?charset=utf8" 
before_parse = 0
after_parse = 1

Base = declarative_base()
class Url(Base):
    __tablename__ = "url"
    id = Column(INTEGER, primary_key=True)
    url = Column(VARCHAR(255))
    createAt = Column(DATETIME)
    content = Column(TEXT)
    depth = Column(INTEGER)
    title = Column(TEXT)
    done = Column(INTEGER)#0:not done 1:done
    isHomePage = Column(INTEGER)#0:not 1:yes

class Db_Method(object):
    def __init__(self):
        engine = create_engine(sql_url)
        DBSession = sessionmaker(bind=engine)
        self.session = scoped_session(DBSession)

    def insert_url(self, url="", content="",
                    depth=0, title="",
                    isHomePage=0):
        now = datetime.datetime.utcnow()
        url = Url(url=url,
                content=content,
                depth=depth,
                title=title,
                createAt=now,
                done=before_parse,
                isHomePage=isHomePage)
        self.session.add(url)
        self.session.commit()
        return url.id

    def get_depth_by_id(self, id):
        sql = self.session.query(Url).\
                        filter(Url.id==id)
        result = self.session.execute(sql)
        if result:
            for item in result:
                depth = item["url_depth"]
                return depth
        return 0

    def update_url(self, id, content="", title=""):
        now = datetime.datetime.utcnow()
        values = { 
                'content': content,
                'title': title,
                'createAt': now,
                'done': after_parse }
        url = self.session.query(Url).\
                filter(Url.id==id).\
                update(values)
        self.session.commit()

    def is_url_exist(self, url):
        count = self.session.query(Url).\
                    filter(Url.url==url).count()
        return count and True or False
        
    def get_url_by_depth(self, depth):
        sql = self.session.query(Url).\
                    filter(Url.depth==depth,
                            Url.done==before_parse)
        result = self.session.execute(sql)
        result_list = []
        for item in result:
            result_list.append((item['url_id'],
                item['url_url']))
        return result_list

    def close_db(self):
        self.session.close()

if __name__ == "__main__":
    db = Db_Method()
#    db.insert_url)
#    db.update_url(3, url="baidul.com")
    print db.is_url_exist("bassidul.com")
    print db.get_url_by_depth(0)

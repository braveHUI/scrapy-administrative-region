# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from nbs.models import Stats,db_connect,create_tables

class NbsPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.session = sessionmaker(bind=engine)()


    def process_item(self, item, spider):
        session = self.session
        post = Stats(area_code=item["area_code"], level=item["level"],area_name=item["area_name"],full_name=item["full_name"],parent=item["parent"])
        try:
            session.add(post)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import hashlib
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class WhiskeyScraperPipeline:
    COLLECTION_NAME = "whiskeys"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_id = self.compute_item_id(item)
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            raise DropItem(f"Duplicate item: {item}")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
            return item
        
    def compute_item_id(self, item):
        name = item["name"]
        return hashlib.sha256(name.encode("utf-8")).hexdigest()

    # def process_item(self, item, spider):
    #     item['description'] = item['description'][0]
    #     return item

    # def __init__(self):
    #         self.conn = mysql.connector.connect(
    #             host = 'localhost',
    #             user = 'root',
    #             password = 'DeathMetal1991$',
    #             database = 'whiskey'
    #         )

    #         self.cur = self.conn.cursor()

    #         self.cur.execute("""
    #         CREATE TABLE IF NOT EXISTS whiskeys(
    #             id int NOT NULL auto_increment,
    #             name VARCHAR(64,
    #             category VARCHAR(32,
    #             distiller VARCHAR(32),
    #             bottler VARCHAR(32),
    #             abv VARCHAR(64),
    #             age VARCHAR(64),
    #             srp VARCHAR(64),
    #             description TEXT,
    #             img VARCHAR(128),
    #             PRIMARY KEY (id)
    #         )
    #         """)

    #     def process_item(self, item, spider):
    #         self.cur.execute(""" insert into whiskeys (name, category, distiller, bottler, abv, age, srp, description, img) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
    #             item['name'],
    #             item['category'],
    #             item['distiller'],
    #             item['bottler'],
    #             item['abv'],
    #             item['age'],
    #             item['srp'],
    #             item['description'],
    #             item['img']
    #         ))

    #         self.conn.commit()

    #     def close_spider(self, spider):
    #         self.cur.close()
    #         self.conn.close()
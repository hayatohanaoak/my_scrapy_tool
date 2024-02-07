# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import sqlite3

class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = f'books_to_scrape/{item.get("UPC")}.jpg'
        return file_name

class BooksToScrapePipeline:
    def open_spider(self, spider):
        self.conn   = sqlite3.connect('practice.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE books_to_scrape (
                titles text,
                prices text,
                stocks int,
                ratings text,
                UPCs text primary key,
                reviews int,
                img_urls text
            );
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.conn.execute('''
            INSERT INTO books_to_scrape (titles, prices, stocks, ratings, UPCs, reviews, img_urls)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        ''',
        (
            item.get('title'),
            item.get('price'),
            item.get('stock'),
            item.get('rating'),
            item.get('UPC'),
            item.get('review'),
            item.get('img_url'),
        ))
        self.conn.commit()
        return item
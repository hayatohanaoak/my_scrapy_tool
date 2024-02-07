# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymongo
import sqlite3

# ImagePipelineの機能を継承し、file_pathメソッドのみオーバーライドするクラスを作る
class customImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = f'computer_books/{item.get("code")}.jpg'
        return file_name

class KinokuniyaPipeline:
    def process_item(self, item, spider):
        # 商品コードがない場合、エラーを出す
        if not item.get('code'):
            raise DropItem('Missing code')
        return item
    
class MongoPipeline:
    collection_name = 'computer_books'
    # spider開始時に呼ばれるopen_spider()を定義
    def open_spider(self, spider):
        # Mongo DBに接続して、BOOKDBを使用する（なければ作る）
        self.client = pymongo.MongoClient('mongodb+srv://test_user:BMBy4MLPRrnGourh@cluster0.ugvq17b.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['BOOKDB']

    # spider終了時に呼び出されるclose_spider()を定義
    def close_spider(self, spider):
        self.client.close()     # 接続を切る

    # 取得データの格納
    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))


class SQLitePipeline:
    def open_spider(self, spider):  # spider開始時は、DB接続
        try:
            self.connection = sqlite3.connect('BOOKDB.db')  # BOOKDB.dbファイルに接続
            self.c = self.connection.cursor()               # カーソルを取得（こいつを介して操作する）
            # クエリ投下
            self.c.execute('''
                /* computer_booksテーブルの作成*/
                CREATE TABLE computer_books(
                    title text,
                    author text,
                    price integer,
                    publisher text,
                    size text,
                    page integer,
                    code text primary key /* 商品コードを主キー*/
                );
            ''')
            # 変更をコミット（反映）
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def process_item(self, item, spider):   # item取得時は、DBへのデータ格納
        self.c.execute('''
            INSERT INTO computer_books (title, author, price, publisher, size, page, code)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        ''',
        # パラメータに代入するものを指定
        (
            item.get('title'),
            item.get('author'),
            item.get('price'),
            item.get('publisher'),
            item.get('size'),
            item.get('page'),
            item.get('code')
        ))
        self.connection.commit()
        return item
    
    def close_spider(self, spider): # 終了時はDB接続を切断
        self.connection.close()
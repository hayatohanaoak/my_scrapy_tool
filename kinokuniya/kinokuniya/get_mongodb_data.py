import pymongo

# mongodbに接続
client = pymongo.MongoClient('mongodb+srv://test_user:BMBy4MLPRrnGourh@cluster0.ugvq17b.mongodb.net/?retryWrites=true&w=majority')
db = client['BOOKDB']
collection = db['computer_books']   # computer_booksテーブルを開く

for doc in collection.find({'size':'B5'}):   # 各ドキュメントを格納
    print(doc)
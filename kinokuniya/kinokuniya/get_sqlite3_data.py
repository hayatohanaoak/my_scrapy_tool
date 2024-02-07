import sqlite3

connection = sqlite3.connect('BOOKDB.db')
cursor = connection.cursor()
for row in cursor.execute('SELECT * FROM computer_books ORDER BY code'):
    print(row)
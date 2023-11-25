import sqlite3 as sl


sqlite = sl.connect('mainLATEST.db')
cursor = sqlite.cursor()

cursor.execute('DELETE from user WHERE sellerid="vaLjwW"')
sqlite.commit()
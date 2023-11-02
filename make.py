import sqlite3 as sl
acc = sl.connect('main.db')

with acc: 
    acc.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            sellerid TEXT NOT NULL,
            phone INTEGER NOT NULL,
            name TEXT,
            address TEXT, 
            city TEXT,
            state TEXT,
            zip TEXT,
            paid INTEGER
        );
    """)  

with acc:
    acc.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            sellerphone INTEGER NOT NULL,
            sellerid TEXT NOT NULL, 
            itemid TEXT NOT NULL, 
            itemprice INTEGER NOT NULL, 
            itemname TEXT NOT NULL,
            itemdisc TEXT,
            itemstatus INTEGER NOT NULL,
            itemcid TEXT NOT NULL
        );
    """)


with acc:
    acc.execute("""
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            event STRING,
            ip STRING,
            useragent STRING,
            time INTGER
        );
    """)

"""Database class"""
import sqlite3 as sl

class DbConnection:
    """
    Class opening and closing database connection
    
    """
    def __init__(self):
        self.conection = None

    def __enter__(self):
        self.conection = sl.connect('database.db')
        return self.conection
    def __exit__(self, conn, value, traceback):
        self.conection.commit()
        self.conection.close()

class DB:
    """
    Class for handling database connections
    
    """
    def create_db(self):
        """
        Makes a database and creates tables if they don't exist

        Returns:
            None
        """
        with DbConnection() as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS user (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        sellerid TEXT NOT NULL
                    );
                """)
            conn.execute("""
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
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS log (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        event STRING,
                        ip STRING,
                        useragent STRING,
                        time INTGER
                    );
                """)

    def insert(self, table, data):
        """
        Inserts data into a table

        Args:
            table (str): Table name
            data (dict): Data to insert

        Returns:
            None
        """
        with DbConnection() as conn:
            conn.execute(f"""
                    INSERT INTO {table} ({', '.join(data.keys())})
                    VALUES ({', '.join(['?']*len(data))})
                """, tuple(data.values()))
    def update(self, table, data, where):
        """
        Updates data in a table

        Args:
            table (str): Table name
            data (dict): Data to update
            where (dict): Where clause

        Returns:
            None
        """
        with DbConnection() as conn:
            conn.execute(f"""
                    UPDATE {table}
                    SET {', '.join([f'{key} = ?' for key in data.keys()])}
                    WHERE {', '.join([f'{key} = ?' for key in where.keys()])}
                """, tuple(data.values()) + tuple(where.values()))
    def delete(self, table, where):
        """
        Deletes data from a table

        Args:
            table (str): Table name
            where (dict): Where clause

        Returns:
            None
        """
        with DbConnection() as conn:
            conn.execute(f"""
                    DELETE FROM {table}
                    WHERE {', '.join([f'{key} = ?' for key in where.keys()])}
                """, tuple(where.values()))
    def select(self, table, where=None):
        """
        Selects data from a table

        Args:
            table (str): Table name
            where (dict): Where clause

        Returns:
            list: List of tuples
        """
        with DbConnection() as conn:
            cursor = conn.cursor()
            if where:
                cursor.execute(f"""
                        SELECT * FROM {table}
                        WHERE {', '.join([f'{key} = ?' for key in where.keys()])}
                    """, tuple(where.values()))
            else:
                cursor.execute(f"""
                        SELECT * FROM {table}
                    """)
            result = cursor.fetchall()
            cursor.close()
            return result

db = DB()
db.create_db()

print(db.select('user'))
db.insert('user', {'sellerid': '1234567890aa'})
print(db.select('user'))
db.update('user', {'sellerid': '0987654321ab'}, {'id': 1})
print(db.select('user'))

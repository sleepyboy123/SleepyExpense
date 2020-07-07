import sqlite3


def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Opened database successfully")
    except FileNotFoundError as e:
        print(e)
    return conn


def main():
    conn = create_connection("expense.db")
    conn.execute('''CREATE TABLE EXPENSE
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    USER INTEGER NOT NULL,
    DESCRIPTION CHAR(50) NOT NULL,
    VALUE REAL NOT NULL); ''')
    print("Table created successfully")
    conn.close()


main()

import sqlite3

conn = sqlite3.connect('Databases/SaldoData.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS SaldoData(
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  VALOR NOT NULL);
                  ''')

print('Connect with DATABASE')
import sqlite3

conn = sqlite3.connect('Databases/DespesasData.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Despesas(
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  NOME NOT NULL,
                  QUANTIDADE NOT NULL,
                  VALOR NOT NULL,
                  CALENDARIO NOT NULL);
                  ''')

print('Connect with DespesasData')
import sqlite3

conn = sqlite3.connect('Databases/DespesasSomaData.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS DespesasSoma(
                  ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  QUANTIDADE NOT NULL,
                  VALOR NOT NULL,
                  CALENDARIO NOT NULL);
                  ''')

print('Connect with DespesasSomadasBD')
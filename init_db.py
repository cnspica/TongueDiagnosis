import sqlite3
import os

db_path = 'AppDatabase.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sql_files = [
    'application/models/create_User.sql',
    'application/models/create_Session.sql',
    'application/models/create_TongueAnalysis.sql',
    'application/models/create_ChatRecord.sql'
]

for sql_file in sql_files:
    with open(sql_file, 'r') as f:
        sql = f.read()
    try:
        cursor.executescript(sql)
        print(f'OK: {sql_file}')
    except Exception as e:
        print(f'ERR {sql_file}: {e}')

conn.commit()
conn.close()

conn2 = sqlite3.connect(db_path)
tables = conn2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables created:', [t[0] for t in tables])
conn2.close()
print('Database initialized successfully!')

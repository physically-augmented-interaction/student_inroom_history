import sqlite3

con = sqlite3.connect("main.db")
cor = con.cursor()
cor.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, student_id VARCHAR, icon_url VARCHAR, is_active INTEGER DEFAULT 1);")
cor.execute("CREATE TABLE room_log(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')));")
con.commit()
con.close()

print("DB CREATED!")
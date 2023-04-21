from sit_idcardlib_py import Reader
import requests
import dotenv
import json
import os
import sqlite3
import datetime
dotenv.load_dotenv()

before_read_student_id = ""
DOMAIN = os.getenv("DOMAIN")

def get_db_connection():
    con = sqlite3.connect("main.db")
    cor = con.cursor()
    return con, cor

def on_room(student_id: str):
    con, cor = get_db_connection()
    cor.execute(f"SELECT * FROM user WHERE student_id = \"{student_id}\";")
    users = cor.fetchall()
    if len(users) == 0:
        return
    cor.execute(f"SELECT id, name FROM user WHERE student_id = \"{student_id}\";")
    user = cor.fetchone()
    datestr = datetime.datetime.now().today().strftime("%Y-%m-%d")
    print(datestr)
    cor.execute(f"SELECT * FROM room_log WHERE user_id = \"{student_id}\" AND created_at BETWEEN \"{datestr} 00:00:00\" AND \"{datestr} 23:59:00\";")
    logs = cor.fetchall()
    print(logs)

    res = requests.post(
        os.getenv("WEBHOOK_URL"),
        json.dumps({
            "username": "room-log-bot", 
            "icon_emoji": ":parrot_rainbow:",
            "channel": "#room-log",
            "text": f"{user[1]}さんが{'来た！' if len(logs)%2 == 0 else '帰った！'}" 
        })
        )
    cor.execute(f"INSERT INTO room_log(user_id) VALUES(\"{student_id}\")")
    con.commit()
    con.close()

def callback(card):
    global before_read_student_id
    if card.id != before_read_student_id:
        print(card.id)
        on_room(card.id)
        before_read_student_id = card.id

reader = Reader(callback)

while True:
    try:
        reader.read()
    except Exception as e:
        print(e)
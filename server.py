from fastapi import FastAPI, HTTPException, status
import sqlite3
import os
import dotenv
import datetime
import requests
import json
import uvicorn

app = FastAPI()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
DOMAIN = os.getenv("DOMAIN")

def get_db_connection():
    con = sqlite3.connect("main.db")
    cor = con.cursor()

    return con, cor



@app.get("/users")
def get_users():
    con, cor = get_db_connection()
    cor.execute("SELECT * FROM user;")
    data = cor.fetchall()
    return [{"id": d[0], "name": d[1], "student_id": d[2], "icon_url": d[3], "is_active": d[4] == 1} for d in data]

@app.post("/users")
def create_user(username: str, student_id: str, icon_url: str):
    con, cor = get_db_connection()
    cor.execute(f"SELECT * FROM user WHERE student_id = \"{student_id}\";")
    data = cor.fetchall()
    if len(data) != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"既に存在する学籍番号です"
            )
    cor.execute(f"INSERT INTO user(name, student_id, icon_url) VALUES(\"{username}\", \"{student_id}\", \"{icon_url}\");")
    con.commit()
    con.close()
    return {"result": "created"}

@app.post("/room_logs")
def create_room_log(student_id: str, token: str):
    con, cor = get_db_connection()
    cor.execute(f"SELECT * FROM user WHERE student_id = \"{student_id}\";")
    users = cor.fetchall()
    if len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"存在しない学籍番号でのリクエストです"
            )
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"指定したTOKENが正しくありません"
            )
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
    return {"result": "created"}

@app.get("/room_logs")
def get_room_logs(day: datetime.date):
    con, cor = get_db_connection()
    cor.execute(f"SELECT * FROM room_log WHERE created_at BETWEEN \"{day} 00:00:00\" AND \"{day} 23:59:00\";")
    data = cor.fetchall()
    con.commit()
    con.close()
    return [{"id": d[0], "user_id": d[1], "created_at": d[2]} for d in data]


uvicorn.run(app=app, host=DOMAIN, port=8000)
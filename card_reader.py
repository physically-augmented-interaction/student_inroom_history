from sit_idcardlib_py import Reader
import requests
import dotenv
import json
import os
dotenv.load_dotenv()

before_read_student_id = ""

def callback(card):
    global before_read_student_id
    if card.id != before_read_student_id:
        print(card.id)
        requests.post(
            f"http://172.21.45.37:8000/room_logs",
            json.dumps({
                "token": os.getenv("TOKEN"),
                "student_id": card.id
            }))
        before_read_student_id = card.id

reader = Reader(callback)

while True:
    try:
        reader.read()
    except Exception as e:
        print(e)
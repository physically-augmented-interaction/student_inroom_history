from sit_idcardlib_py import Reader

before_read_student_id = ""

def callback(card):
    global before_read_student_id
    if card.id != before_read_student_id:
        print(card.id)
        before_read_student_id = card.id

reader = Reader(callback)

while True:
    try:
        reader.read()
    except Exception as e:
        print(e)
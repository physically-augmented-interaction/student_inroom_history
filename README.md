## Install

```sh
sudo pip3 install nfcpy==1.0.3
pip3 install -r requirements.txt
```

`.env.sample`を参考に`.env`を作成してください。（任意の文字列が使用可能です）

## Run

```sh
python3 server.py
sudo python3 card_reader.py
```

## DB

### user

Name | Type | Kind
:-: | :-: | :-:
id | INT | PRIMARY KEY AUTOINCREMENT
name | VARCHAR | 
student_id | VARCHAR | UNIQUE
icon_url | VARCHAR | 
is_active | INT | DEFAULT 1

### room_log

Name | Type | Kind
:-: | :-: | :-:
id | INT | PRIMARY KEY AUTOINCREMENT
user_id | INT | 
created_at | TEXT |
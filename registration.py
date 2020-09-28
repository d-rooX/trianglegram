import sqlite3
import json


def start():
    db = sqlite3.connect('Account.sqlite3')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Account (
	    ID INTEGER PRIMARY KEY,
	    API_ID TEXT,
	    API_HASH TEXT,
	    NAME TEXT,
	    FRIEND_ID TEXT,
	    MY_ID TEXT
        )""")
    db.commit()
    cur.execute("""SELECT * FROM Account WHERE ID = 1""")
    result = cur.fetchone()

    if result:
        _, api_id, api_hash, name, _, _ = result
        print(f'Найдена запись с name = {name} api_id = {api_id}\nЧтобы выбрать другую, удалите Account.sqlite3')
    else:
        api_id = input("Api_id: ")
        api_hash = input("Api_hash: ")
        name = input("@username собеседника: ")
        cur.execute("INSERT INTO Account(API_ID, API_HASH, NAME) VALUES (?,?,?);",
                    (api_id, api_hash, name))
        db.commit()

    password = input("Введи общий пароль, с вашим собеседником: ")

    first_json = {'cover': '', 'secret': '', 'password': password, 'output': 'encrypted_msg.txt'}
    second_json = {'cover': '', 'password': password, 'output': 'recieved.txt'}

    with open("to_send.json", 'w') as json1:
        json1.write(json.dumps(first_json))

    with open("recieved.json", 'w') as json2:
        json2.write(json.dumps(second_json))

    return api_id, api_hash, name, password

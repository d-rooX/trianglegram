import asyncio
from telethon import events, TelegramClient, sync
import sqlite3
import time
from tkinter import *
import threading
import json
import os
from lorem_text import lorem


class Trianglegram:
    def __init__(self, api_id, api_hash, name):

        self.client = TelegramClient("first", api_id, api_hash)
        self.client.start()
        time.sleep(1)

        self.my_id = self.client.get_me().id
        self.friend_id = self.client.get_entity(name).id
        
        # подключение к бд
        self.db = sqlite3.connect('Account.sqlite3')
        self.cur = self.db.cursor()

        self.cur.execute(f'UPDATE Account SET MY_ID = ?, FRIEND_ID = ? WHERE ID = ?',
                             (str(self.my_id), str(self.friend_id), 1))
        self.db.commit()

        # отрисовка окна
        self.window = Tk()
        self.messages = Text(self.window)
        self.input_user = StringVar()
        self.input_field = Entry(self.window, text=self.input_user)
        self.frame = Frame(self.window)
        self.frame.pack()
        self.messages.pack()
        self.input_field.pack(side=BOTTOM, fill=X)
        self.input_field.bind("<Return>", self.enter_pressed)

    # колбек для поля ввода
    def enter_pressed(self, event):
        input_get = self.input_field.get()

        print("Зашифровка")

        cover = lorem.sentence()
        with open("to_send.json") as f:
            buffer = f.read()

        cryptor_data = json.loads(buffer)
        cryptor_data["cover"] = cover
        cryptor_data["secret"] = input_get

        with open("to_send.json", 'w') as f:
            f.write(json.dumps(cryptor_data))

        os.system("stegcloak hide --config to_send.json")

        print("Отправка шифровки")

        self.cur.execute(f"SELECT NAME FROM Account WHERE ID = '{1}'")
        name = str(self.cur.fetchone()[0])

        async def main():
            with open("encrypted_msg.txt", "r") as enc_msg_file:
                data_to_send = str(enc_msg_file.read())
            await self.client.send_message(name, data_to_send)

        self.client.loop.run_until_complete(main())
        self.messages.insert(INSERT, '%s\n' % input_get)
        self.input_user.set('')
        return "break"


def start(api_id, api_hash, name):

    triangle = Trianglegram(api_id, api_hash, name)

    def run_bot_events():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_run_events(loop))

    async def async_run_events(loop):
        eventing_client = await TelegramClient("second", api_id, api_hash, loop=loop).start()

        @eventing_client.on(events.newmessage.NewMessage(from_users=triangle.friend_id))
        async def handler(event):
            message = event.message.message
            if message is not None:
                with open("recieved.json") as rcv_msg_file:
                    recieved_message = rcv_msg_file.read()
                json_obj = json.loads(recieved_message)
                json_obj["message"] = str(message)

                with open("recieved.json", 'w') as rcv_msg_file:
                    rcv_msg_file.write(json.dumps(json_obj))

                os.system("stegcloak reveal --config recieved.json")

                with open("recieved.txt", "r") as rcv_msg_file:
                    data = rcv_msg_file.read()

            triangle.messages.insert(INSERT, f'{data}\n')

        await eventing_client.run_until_disconnected()

    threading.Thread(target=run_bot_events).start()
    triangle.window.mainloop()

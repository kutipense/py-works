#!/usr/bin/env python3
#-*- coding=utf-8 -*-
from functions.pNumber_query import participant_info
from functions.uid_increment import uid_increment
from functions.session_reset import session_reset
from functions.registration import registration
from functions.uid_query import uid_query

import socket
import threading
import sqlite3 as sql

# Database
db = sql.connect('liste1.db3', check_same_thread=False)
cursor = db.cursor()

# Thread Lock
lock = threading.Lock()

# Server
SERVER = ('0.0.0.0', 5000)  # IP,PORT
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(SERVER)
s.listen(5)


def init_db():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS participant_list (phoneNumber PRIMARY KEY\
        ,name,mail,school,department,grade,uid,counter INTEGER,control INTEGER)")
    db.commit()


def locker(function):
    def wrapper(*args, **kwargs):
        lock.acquire()
        a = function(*args, **kwargs)
        lock.release()
        return a
    return wrapper

func = {
    'kayit': registration,
    'tel_sorgu': participant_info,
    'uid_sorgu': uid_query,
    'uid_artir': uid_increment,
    'oturum': session_reset,
}


@locker
def clHandler(sck, ip):
    try:
        address = "[%s]" % ip
        while True:
            data = str(sck.recv(1024), encoding='utf-8')
            args = data.split(';')
            if data:
                print('[+] %s' % data, address)
            islem = func.get(args[0])(*args[1:], cursor=cursor)
            sck.send(bytes(str(islem), encoding='utf-8'))
            print('[-] %s' % islem, address)
            db.commit()
    except ConnectionResetError:
        pass
    finally:
        print('[-]', address)
        db.commit()
        sck.close()


if __name__ == '__main__':
    init_db()
    try:
        print('started...')
        while True:
            cl, addr = s.accept()
            print('[+]', '[%s]' % addr[0])
            cl_thread = threading.Thread(target=clHandler, args=(cl, addr[0]))
            cl_thread.start()
    finally:
        print('\nÇıkılıyor....')
        s.close()
        db.close()

#-*- coding=utf-8 -*-
import socket
import threading
import sqlite3 as sql
import uuid

#Database
db = sql.connect('liste.db3',check_same_thread=False)
im = db.cursor()

#Thread Lock
lock = threading.Lock()

#Server
SERVER = ('0.0.0.0',5000) #IP,PORT
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(SERVER)
s.listen(5)


def init_db():
	im.execute("CREATE TABLE IF NOT EXISTS liste (telefon PRIMARY KEY,isim,mail,okul,bolum,sinif,uid,sayac INTEGER,kontrol INTEGER)")
	db.commit()

def locker(function):
	def wrapper(*args,**kwargs):
		lock.acquire()
		a = function(*args,**kwargs)
		lock.release()
		return a
	return wrapper

@locker #telefon, isim, mail, okul, bolum, sinif, uid # kayit;1;2;3;4;5;6;7
def kayit(*args,sayac=0,kontrol=0):
    im.execute("SELECT * FROM liste WHERE uid = ?",(args[-1],))
    sorgu = im.fetchone()
    ret = 'Güncellendi!'
    if sorgu==None:
        im.execute("SELECT * FROM liste WHERE telefon = ?",(args[0],))
        sorgu2 = list(im.fetchone())
        if sorgu2!=None:
            im.execute("DELETE FROM liste WHERE telefon = ?",(args[0],))
            sorgu2[-3] = args[-1]
            im.execute("INSERT INTO liste VALUES (?,?,?,?,?,?,?,?,?)",(*sorgu2,))
            ret = 'Yeni kart kaydedildi'
		
        else:
            im.execute("INSERT INTO liste VALUES (?,?,?,?,?,?,?,?,?)",(*args,sayac,kontrol))
            ret = 'Kaydedildi!'

    elif len(sorgu[0])==10 and sorgu[0]!=args[0]:
        ret = 'Kullanılmış kart!'
    elif len(sorgu[0])>10:
        im.execute("DELETE FROM liste WHERE uid = ?",(args[-1],))
        im.execute("INSERT INTO liste VALUES (?,?,?,?,?,?,?,?,?)",(*args,sorgu[-2],sorgu[-1]))
    else:
        im.execute("""UPDATE liste SET isim = ?, mail = ?,okul = ?, bolum = ?, sinif = ? WHERE uid = ?""",(*args[1:-1],args[-1]))
    db.commit()
    return ret

@locker		
def tel_sorgu(*args):
	im.execute("SELECT * FROM liste WHERE telefon = ?",(args[0],))
	sorgu = im.fetchone()
	if sorgu==None:
		im.execute("SELECT * FROM liste WHERE uid = ?",(args[1],))
		sorgu = im.fetchone()
	return ';'.join(sorgu[1:-2]) if sorgu!=None else 'Bulunamadı!'

@locker
def uid_sorgu(*args):
	im.execute("SELECT sayac FROM liste WHERE uid = ?",(args[0],))
	sorgu = im.fetchone()
	return str(sorgu[0]) if sorgu!=None else 'Kayıt bulunamadı!'

@locker
def uid_artir(*args):
	im.execute("SELECT sayac,kontrol FROM liste WHERE uid = ?",(args[0],))
	sorgu = im.fetchone()
	if sorgu==None:
		k_ö = str(uuid.uuid1())
		im.execute("INSERT INTO liste VALUES (?,'k.ö','k.ö','k.ö','k.ö','k.ö',?,?,?)",(k_ö,args[0],1,1))
		db.commit()
		return 'Geçersiz kayit!'
	elif sorgu[1]==0:
		im.execute("UPDATE liste SET sayac = ?, kontrol = 1 WHERE uid = ?",(sorgu[0]+1,args[0]))
		db.commit()
		return 'Sayaç bir(1) artırıldı! [%d]' % (sorgu[0]+1)
	return 'Geçersiz işlem!'

@locker
def oturum(*args):
	im.execute("UPDATE liste SET kontrol = 0")
	db.commit()
	return 'Oturum Değiştirildi'
	
func = {'kayit' : kayit,
		'tel_sorgu' : tel_sorgu,
		'uid_sorgu' : uid_sorgu,
		'uid_artir' : uid_artir,
		'oturum': oturum
		}

def clHandler(sck,ip):
	try:
		while True:
			data = str(sck.recv(1024),encoding='utf-8')
			args = data.split(';')
			if data:
				print('[+]',data,'received from',ip,end=' ~ ')
			islem = func.get(args[0])(*args[1:])
			
			sck.send(bytes(str(islem),encoding='utf-8'))
			print('İşlem yapıldı.','~~~['+islem+']',sep='\n')
	except TypeError:
		print('>>>',ip,'\'den geçersiz veri alındı!')
	except ConnectionResetError:
		print('>>>',ip,' bağlantıyı kesti!')
	finally:
		print('>>>',ip,'\'nin soketi kapatılıyor...')
		sck.close()


if __name__ == '__main__':
	init_db();print('DB initialized')
	try:
		print('SERVER HAS STARTED!\n%s'%('-'*50))
		threading.Semaphore(1)
		while True:
			cl, addr = s.accept()
			print('[+]',addr[0], 'connected!')

			cl_thread = threading.Thread(target=clHandler, args=(cl,addr[0]))
			cl_thread.start()
	finally:
		print('\nÇıkılıyor....')
		s.close()
		db.close()

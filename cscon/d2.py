import json
import requests
import socket

temp = 'http://api.fixer.io/latest?base={}'
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1',5000))
s.listen(5)


def main(c):
	mik,x,y = c.recv(100).strip().split()
	data = requests.get(temp.format(str(x)[2:-1]))
	data = json.loads(data.text)
	print(data["rates"][str(y)[2:-1]])
	c.send(b"%f" %(float(str(mik)[2:-1])*float(data["rates"][str(y)[2:-1]]),))

if __name__ == '__main__':
	while True:
		c,addr=s.accept()
		main(c)
		c.close()
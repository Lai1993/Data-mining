import os
import socket
import select

HOST = ''
PORT = 5555
ADDR = (HOST,PORT)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(ADDR)

filename = ''
while True:
	data = s.recv(SIZE)
	if not data:
		print('reach the end of file')
		break
	elif filename == '':
		filename = data
		list = os.listdir('.')
		for iterm in list:
			if iterm == data:
				os.remove(iterm)
				print('remove')
			else:
				pass
		with open('./'+data,'wb')as f:
			pass
	else:
		with open('./'+data,'ab')as f:
			f.write(data)
s.close()
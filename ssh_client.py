import threading 
import socket
import os
import pickle
from encryption import *

connect=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect.connect(("127.0.0.1",6002))
workin_directory='/home/surgan'
dh=DH()

prime=connect.recv(4096)
prime=int(prime)

generator=connect.recv(4096)
generator=int(generator)

pub_2=connect.recv(4096)
pub_2=int(pub_2)
pvt_2=dh.get_private_key()

pub_self=dh.gen_public_key(prime,generator)
connect.sendall(str(pub_self))

shared_key=dh.gen_shared_key(pub_2,prime)
print(shared_key)
o2=AESCipher(shared_key)
pas=input()
pas=o2.encrypt(pas)
connect.sendall(pas)
print(pas)
print(connect.recv(4096))

workin_directory=o2.encrypt(workin_directory)
connect.sendall(workin_directory)

while (True):
	p=input()
	
	g=p.strip()
	h=g.split(' ')
	send=o2.encrypt(p)
	connect.sendall(send)
	
	
	while(True):
		r=connect.recv(4096)
		r=o2.decrypt(r)
		print(r)
		if len(r)<4096:
			break

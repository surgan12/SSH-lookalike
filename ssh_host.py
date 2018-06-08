import threading 
import os
import socket
import pickle
import time
import hashlib
import subprocess 
from threading import *
import signal
from encryption import *
password="password"

def login(pas,pas_given):								#login-authentication.
	if (pas==pas_given):
		return 1
	else:
		return 0

def client_handle(socket):
	exit="exit"
	change_dir="cd"	
	pre=".."
	home="--"
	dh=DH()		 #KEY EXCHANGE USING DIFFIE-HELLMAN ALGORITHM
	prime=dh.p

	socket.sendall(str(prime ))			

	generator=dh.g
	socket.sendall(str(generator))

	pvt=dh.get_private_key()
	
	pub=dh.gen_public_key(prime,generator)
	
	socket.sendall(str(pub))
	
	pub_2=socket.recv(1024)
	pub_2=int(pub_2)
	
	shared_key=dh.gen_shared_key(pub_2,prime)	#generating shared key
	print(shared_key)
	
	o1=AESCipher(shared_key)
	pas=socket.recv(4096).decode()
	pas_given=o1.decrypt(pas)
	print(pas)
	f=login(pas_given,password)
	print(f) #checking the login 
	if f!=1:
		socket.close()
	else:
		socket.sendall("successful connection")
		direc=socket.recv(1024)
		directory=o1.decrypt(direc)
		print(directory)
		while (True):
		
			os.chdir(directory)
			command=socket.recv(4096)
			command=o1.decrypt(command)
			command=command.decode()
			lis=command.strip()
			lis=lis.split(' ')
			if lis[0]==change_dir:
			
				if(lis[1]==pre):
					get_pre=directory.split('/')
					directory='/'
					for i in range(1,len(get_pre)-1):
						directory=directory+get_pre[i]+'/'
					os.chdir(directory)
					enc=o1.encrypt(directory)
					socket.sendall(enc)

				elif(lis[1]==home):
					os.chdir('/home/surgan/')
					directory='/home/surgan/'
					enc=o1.encrypt(directory)
					socket.sendall(enc)
				else:
			
					directory=directory+'/'+lis[1]
					os.chdir(directory)
					enc=o1.encrypt(directory)
					socket.sendall(enc)
			elif lis[0]==exit:
				socket.close()
				

			else:
				command=command.split(' ')
				op = subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE, stdout=subprocess.PIPE)	
				Timer(5, op.send_signal, [signal.SIGINT]).start() # Ctrl+C in 5 seconds
				out, err = op.communicate() 
				if out:
					enc=o1.encrypt(out.decode())
					socket.sendall(enc)
					
				elif err:
					enc=o1.encrypt(err.decode())
					socket.sendall(enc)
				else:
					socket.sendall("0")
			

host='127.0.0.1'
port=6002
listen_port=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_port.bind((host,port))
listen_port.listen(10)
online=[]
while(True):
	client,addr=listen_port.accept()
	t1=threading.Thread(target=client_handle,args=(client,))
	t1.start()

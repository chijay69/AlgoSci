""" A client module"""

import socket
import sys


def wait_and_read(client_obj):
	try:
		# reads the user input
		line = sys.stdin.readline().rstrip('\x00') # strips x00 from EOL
		# ncode the input and send it to server
		client_obj.sendall(line.encode('utf-8'))
	except Exception as e:
		print(f'{e} occured')


		
def client_connect(address):
	try:
		# create a socket (SOCK_STREAM means a TCP socket)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			# Connect to the server and send data
			try:
				#ip, port = address
				sock.connect(address)
				print("\nEnter search keyword:\n")
				while True:
					try:
						wait_and_read(sock)
					except TypeError:
						print('No argument was passed to function')
					while True:
						try:
							recieved = sock.recv(1024).decode('utf-8')
							print(recieved, end="")
							if len(recieved) < 1024:
								break
						except:
							sock.close()
			except TypeError as t:
				print(f"got {type(address)} instead of tuple.\nDid you pass host_ip and port as argument?")
				print(t)
			
	except ConnectionRefusedError:
		print("Cannot establish connection due to Server not accepting connections")

	
		 
def start_client(address):
	try:
		try:
			client_connect(address)
		except TypeError:
			print("Could not start up client.")
			print('Ensure argument was passed to function')	
	except KeyboardInterrupt:
		sys.exit(0)
		
		



if __name__ =='__main__':
	host = "localhost"
	port = 49995
	address = (host, port)
	start_client(("localhost",49995))


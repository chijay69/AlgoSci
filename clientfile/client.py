""" A client module"""

import socket
import sys

		
def client_connect(address):
	try:
		# create a socket (SOCK_STREAM means a TCP socket)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			# Connect to the server and send data
			try:
				ip, port = address
				sock.connect((ip, port))
				print("\nEnter search keyword:\n")
				while True:
					line = sys.stdin.readline().strip('\x00')
					if not line:
						break
					sock.sendall(line.encode('utf-8'))
					while True:
						# Recieve data from the server 
						recieved = sock.recv(1024).decode('utf-8')
						print(recieved, end="")
						if len(recieved) < 1024:
							break
			except TypeError:
				print(f"got {type(address)} instead of tuple.\nDid you pass host_ip and port as argument?")
			
	except ConnectionRefusedError:
		print("Cannot establish connection due to Server not accepting connections")

	
		 
		
address = ("localhost", 49995)
client_connect(address)

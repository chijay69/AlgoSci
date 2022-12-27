""" A server module"""

import time
import logging
import threading
import socketserver
from configparser import ConfigParser

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

# initialise config object
config = ConfigParser()

# read config file
config.read("/root/AlgoSci/config.ini")
algosci = config["ALGOSCI"]

try:
	# get config values
	PORT = int(algosci["port"])
	HOST = algosci["host"]
	REREAD_ON_QUERY = algosci.getboolean("reread_on_query")
	filepath = algosci.get("linuxpath")

except (KeyError, ValueError, NameError):
	print("Cannot Parse configuration, check config file")
	# raise Exception

def search_text(file_path, search_key):
	if not search_key.endswith(' '):
		if (search_key !=''):
			try:
				with open(file_path) as inF:
					for line in inF:
						if search_key in line:
							return True
					return False
			except NameError:
				print ('File does not exist, please comfirm file path')
	return False
		

class ThreadedFileRequestHandler(socketserver.StreamRequestHandler):
	def __init__(self, request, client_address, server):
		self.logger = logging.getLogger('ThreadedFileRequestHandler DEBUG')
		self.logger.debug('__init__')
		socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
		return
		
	def setup(self):
		self.logger.debug('setup')
		return socketserver.StreamRequestHandler.setup(self)
		
	def handle(self):
		self.logger.debug('handle')

		# client
		try:
			ip, port = self.client_address
		except :
			print('Ensure ip and port address are provided')
			
		client = f"{ip} connected on {threading.current_thread().name}"
		self.logger.debug(f'DEBUG: {client}')
		
		# accepts string from client connecction
		while True:
			string = self.rfile.readline().decode('utf-8')
			self.logger.debug('recv() => "%s"', string)
			if not string:
				break
			# get the execution time
			start = time.monotonic_ns()
			string = string.strip('\n')
			conditional = search_text(filepath, string)
			end = time.monotonic_ns()
			if conditional:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
				self.wfile.write(b"STRING EXISTS\n")
			else:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
				print('execution time: {}ms'.format((end - start)//1000000))
				self.wfile.write(b"STRING NOT FOUND\n")
		self.logger.debug(f"{self.client_address} closed connection")
		
	def finish(self):
		self.logger.debug('finish')
		return socketserver.StreamRequestHandler.finish(self)
		
		
class ThreadedFileServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	def __init__(self, server_address, handler_class=ThreadedFileRequestHandler):
		self.logger = logging.getLogger('ThreadedFileServer DEBUG')
		self.logger.debug('__init__')
		socketserver.TCPServer.__init__(self, server_address, handler_class)
		return
	
	daemon_threads =True
	allow_reuse_address = True
	logging =  True
	
	
def start_server(address):		
	try:
		with ThreadedFileServer(address, ThreadedFileRequestHandler) as server:
			print("Server is running...")
			server.serve_forever()
	except Exception as e:
		print(f'An Exception {e} Occured')


if __name__ =='__main__':
	host = "127.0.0.1"
	port = 49995
	address = (host, port)
	start_server(address)

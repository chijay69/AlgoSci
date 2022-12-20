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
config.read("/home/liveuser/Documents/AlgoSci//config.ini")
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
	try:
		with open(file_path) as inF:
			for line in inF:
				if search_key in line:
					return True
			return False
	except NameError:
		print ('File does not exist, please comfirm file path')
		

class ThreadedFileRequestHandler(socketserver.StreamRequestHandler):
	def __init__(self, request, client_address, server):
		self.logger = logging.getLogger('ThreadedFileRequestHandler')
		self.logger.debug('__init__')
		socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
		return
		
	def setup(self):
		self.logger.debug('setup')
		return socketserver.StreamRequestHandler.setup(self)
		
	# please help test this function	
	def handle(self):
		self.logger.debug('handle')

		# client
		try:
			ip, port = self.client_address
			assert(ip is not None and type(ip) is str)
			assert(ip is not None and type(ip) is int)
		except AssertionError:
			print('Ensure ip is a string and port is an integer')
			
		client = f"{ip} connected on {threading.current_thread().name}"
		self.logger.debug(f'DEBUG: {client}')
		print(f'DEBUG: {client}')
		
		# accepts string from client connecction
		while True:
			string = self.rfile.readline().decode('utf-8')
			self.logger.debug('recv() => "%s"', string)
			if not string:
				break
			# get the execution time
			start = time.monotonic_ns()
			try:
				conditional = search_text(filepath, string)
			except TypeError:
				print('Two argument are required, one was given')
			end = time.monotonic_ns()
			if conditional:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
				print('DEBUG: execution time: {}ms'.format((end - start)//1000000))
				self.wfile.write(b"STRING EXISTS\n")
			else:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
				print('DEBUG: execution time: {}ms'.format((end - start)//1000000))
				self.wfile.write(b"STRING NOT FOUND\n")
		print(f"DEBUG: {self.client_address} closed connection")
		
	def finish(self):
		self.logger.debug('finish')
		return socketserver.StreamRequestHandler.finish(self)
		
		
class ThreadedFileServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	def __init__(self, server_address, handler_class=ThreadedFileRequestHandler):
		self.logger = logging.getLogger('ThreadedFileServer')
		self.logger.debug('__init__')
		socketserver.TCPServer.__init__(self, server_address, handler_class)
		return
	
	daemon_threads =True
	allow_reuse_address = True
	logging =  True
	

try:
	with ThreadedFileServer(("localhost", 49995), ThreadedFileRequestHandler) as server:
		print("Server is running...")
		server.serve_forever()
except Exception as e:
	print(f'An Exception {e} Occured')

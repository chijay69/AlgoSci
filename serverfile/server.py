""" A server module"""

import time
import logging
import threading
import socketserver
from configparser import ConfigParser

# initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

# initialise config object
config = ConfigParser()

# create empty set
my_set = set()


def search_text(file_path, search_key):
	'''A function that seaches through a file for a search_key'''
	# initialize global variable
	global my_set
	# checks if the search_key is empty or filled with spaces
	if not search_key.endswith(' ') and (search_key !=''):
		# use a try except block to catch exceptions and handle accordingly
		try:
			# open a file 
			with open(file_path) as f:
				# create a loop
				while True:
					# read a line and add the line to a set
					my_set.add(f.readline().rstrip())
					# checks if no more lines to read
					if not f.readline():
						# breaks the loop if the check worked
						break
			# checks if search_key is in the set
			if search_key in my_set:
				# returns true if it checks out
				return True
		# catches name error exception
		except NameError:
			# handle the exception
			print ('File does not exist, please comfirm file path')
	# return false if the search key could not be found
	return False
		

class ThreadedFileRequestHandler(socketserver.StreamRequestHandler):
	def __init__(self, request, client_address, server):
		self.logger = logging.getLogger('ThreadedFileRequestHandler DEBUG')
		self.logger.debug('__init__')
		socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
		
	def setup(self):
		self.logger.debug('setup')
		return socketserver.StreamRequestHandler.setup(self)
		
	def handle(self):
		'''A handle function to handle the logic in the socket server'''
		self.logger.debug('handle')

		# opens a try except block
		try:
			# get the ip address and port of the connected client
			ip, port = self.client_address
		except :
			print('Ensure ip and port address are provided')
			
		client = f"{ip} connected on {port} on {threading.current_thread().name}"
		self.logger.debug(f'{client}')
		
		# accepts string from client connecction
		while True:
			# opens a try except block
			try:
				# read config file
				config.read("/home/unix/AlgoSci/config.ini")
				algosci = config["ALGOSCI"]
				# get config values
				REREAD_ON_QUERY = algosci.getboolean("reread_on_query")
				filepath = algosci.get("linuxpath")
			except (KeyError, ValueError, NameError):
				print("Cannot Parse configuration, check config file")

			# read the string entered by the client
			string = self.rfile.readline().decode('utf-8')

			self.logger.debug('recv() => "%s"', string)

			# checks if a string was sent
			if not string:
				# if no string was found break the loop
				break

			# strip the sring of newline character
			string = string.strip('\n')
			# get the execution time
			start = time.monotonic_ns()

			# check if flag is set to True
			if REREAD_ON_QUERY == True:
				# if true read from file, call search_text function
				conditional = search_text(filepath, string)
			else:
				# if false read from set
				conditional = string in my_set

			end = time.monotonic_ns()

			# checks if conditional is True or False
			if conditional:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
				self.wfile.write(b"STRING EXISTS\n")
			else:
				self.logger.debug('execution time: {}ms'.format((end - start)//1000000))
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
	
	daemon_threads =True
	allow_reuse_address = True
	logging =  True
	
	
def start_server(address):
	'''Function that starts the server '''
	# opens a try except block
	try:
		# create server instance 
		with ThreadedFileServer(address, ThreadedFileRequestHandler) as server:
			print("Server is running...")
			# keep the server running 
			server.serve_forever()
	except ConnectionError:
		print('Could not start server')


if __name__ =='__main__':
	# set ip address and port number to be bound
	address = ("127.0.0.1", 49995)
	# call start server function to start the server
	start_server(address)

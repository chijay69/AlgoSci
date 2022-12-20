import sys
import time
import pytest
import socket
import logging
import threading
import socketserver
from configparser import ConfigParser

from server import ThreadedFileRequestHandler, ThreadedFileServer, search_text
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')


class TestServer:
	
	def test_connection(self):
		logger = logging.getLogger('TestServer')
		self.file_server = ThreadedFileServer(("localhost",7777), ThreadedFileRequestHandler)
		self.ip, self.port = self.file_server.server_address # find out what port we were given
		assert(self.ip == "127.0.0.1")
		assert(self.port == 7777)
		logger.info('Server on %s:%s', self.ip, self.port)
		self.server_thread = threading.Thread(target=self.file_server.serve_forever)
		self.server_thread.deamon_threads = True # don't hang on exit
		self.server_thread.start()
		logger = logging.getLogger('client')
		# This is our fake test client that is just going to attempt a connect and disconnect
		logger.debug('creating client')
		self.fake_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.fake_client.connect(("localhost",7777))
		self.fake_client.close()
		self.file_server.socket.close()
		
	def test_search(self):
		self.search_key = 'boy'
		
		with open('test.txt', 'w') as f:
			f.write('Hey! it is a boy.')
			
		assert search_text('test.txt', self.search_key)
	
	def test_shutdown(self):
		# Issue #2302: shutdown() should always succeed in making an
		# other thread leave serve_forever().
		threads = []
		for i in range(100):
			s = ThreadedFileServer(("localhost", 0), ThreadedFileRequestHandler)
			t = threading.Thread(
			name='MyServer serving',
			target=s.serve_forever,
			kwargs={'poll_interval':0.01})
			t.daemon = True  # In case this function raises.
			threads.append((t, s))
		for t, s in threads:
			print(t, s)
			t.start()
			s.shutdown()
		for t, s in threads:
			print(t, s)
			t.join()
			s.server_close() 

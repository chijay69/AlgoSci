#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  serverUpper.py
#  
#  Copyright 2022 Live System User <liveuser@localhost-live>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import threading
import socket
import socketserver

class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		# Echo back to the client
		data = self.request.recv(1024)
		data = data.decode('utf-8')
		cur_thread = threading.current_thread()
		response = '%s, %s' %(cur_thread.name, data.upper())
		self.request.send(response.encode('utf-8'))
		return
		
class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	deamon_threads = True
	allow_reuse_address =True



if __name__ == '__main__':
    
    address = ('localhost', 0) # let the kernel give us a port
    server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
    ip, port = server.server_address # find out what port we were given

    t = threading.Thread(target=server.serve_forever)
    t.start()
    print ('Server loop running in thread:', t.name)

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    message = 'Hello, world'
    print ('Sending : "%s"' % message)
    len_sent = s.send(message.encode('utf-8'))

    # Receive a response
    response = s.recv(1024)
    print ('Received: "%s"' % response.decode('utf-8'))

    # Clean up
    s.close()
    server.socket.close()

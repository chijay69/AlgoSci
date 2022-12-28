import socket
import threading
import pytest
import socketserver

from serverfile.store.client import client_connect, wait_and_read


def run_fake_server():
    # Run a server to listen for a connection and then close it
    server_sock = socket.socket()
    server_sock.bind(('127.0.0.1', 7777))
    server_sock.listen(0)
    server_sock.accept()
    server_sock.close()
    
def test_client_connects_and_disconnects_to_default_server():
    # Start fake server in background thread
    server_thread = threading.Thread(target=run_fake_server)
    server_thread.start()

    # Test the clients basic connection and disconnection
    address = ('127.0.0.1', 7777)
    game_client = client_connect(address)
    # game_client.disconnect()

    # Ensure server thread ends
    server_thread.join()

def test_wait_and_read():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 49995))
	pass

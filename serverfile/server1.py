import asyncio
import time
import logging
import threading
import socketserver
from configparser import ConfigParser


logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')


# initialise config object
config = ConfigParser()

# read config file
config.read("/home/liveuser/Documents/AlgoSci/config.ini")
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


async def handle_echo(reader, writer):
	logger = logging.getLogger('handle_echo DEBUG')
	try:
		while True:
			try:
				data = await reader.read(1024)
				message = data.decode('utf-8').rstrip('\n')
				addr = writer.get_extra_info('peername')
			except:
				print("No data available to be read")
			
			
			reply = f"Received {message!r} from {addr!r}"
			logger.debug(reply)
			
			start = time.monotonic_ns()
			conditional = search_text(filepath, message)
			end = time.monotonic_ns()
			
			print('execution time: {}ms'.format((end - start)//1000000))
			if conditional:
				writer.write(b"STRING EXISTS\n")
				await writer.drain()
			else:
				writer.write(b"STRING NOT FOUND\n")
				await writer.drain()
	except ConnectionError:
		print("Client connection was terminated")


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

first = time.monotonic_ns()
asyncio.run(main())
last = time.monotonic_ns()
print('main execution time: {}ms'.format((last - first)//1000000))

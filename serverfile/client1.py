"""A client module"""

import sys
import asyncio


def read_msg():
	try:
		# reads the user input
		line = sys.stdin.readline().rstrip('\x00') # strips x00 from EOL
		return line
	except Exception as e:
		print(f'{e} occured')
		
	
		
		
async def tcp_echo_client():
	try:
		reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
	except ConnectionError:
		print("Could not establish connection, Ensure address was passed.")
	
	while True:
		message = read_msg()
		if not message:
			break
		writer.write(message.encode('utf-8'))
		await writer.drain()

		data = await reader.read(100)
		print(data.decode('utf-8'))


asyncio.run(tcp_echo_client())

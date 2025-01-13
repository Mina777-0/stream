'''async def create_connection(message):
    reader, writer= await asyncio.open_connection('127.0.0.1', 8888)

    print(f"Send: {message !r}")
    writer.write(message.encode())
    await writer.drain()

    data= await reader.read(100)
    print(f"Received Data: {data.decode()!r}")

    print("Closw connection")
    writer.close()
    await writer.wait_closed()

asyncio.run(create_connection("Hello World"))'''


'''# Handle a client and server 
async def handle_client(reader, writer):
    data= await reader.read(100)
    message= data.decode()
    addr= writer.get_extra_info('peername')

    print(f"Recieved {message!r} from {addr!r}")

    response= f"Echo: {message}"
    print(f"Send: {response!r}")
    writer.write(response.encode())
    await writer.drain()

    print("Close connection")
    writer.close()
    await writer.wait_closed()

# Start a server
async def main():
    # Start a server, listening on 127.0.0.1 port 8888
    server= await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    addr= server.sockets[0].getsockname()
    print(f"Server on {addr}")

    async with server:
        await server.serve_forever()


# Handle message from the client 
async def client_connection(message):
    await asyncio.sleep(1)
    reader, writer= await asyncio.open_connection('127.0.0.1', 8888)

    print(f"Sending {message}")

    writer.write(message.encode())
    await writer.drain()

    data= await reader.read(100)
    print(f"Reveived: {data.decode()}")

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


async def handle_connection():
    await asyncio.gather(main(), client_connection("Hello server"))

asyncio.run(handle_connection())'''
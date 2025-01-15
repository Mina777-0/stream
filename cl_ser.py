import asyncio


# Create a full-duplex communication like pager

'''
A client connect to the server socket through asyncio.open_connection('127.0.0.1',8888). The server already started by asyncio.start_server()
asyncio.star_server(handle_client, '127.0.0.1', 8888) this connect the server with the function(software) to handle the received messages and control the traffic
whether to broadcast in case of many clients or respond to the sender by confirming the message recieved.
When a cleint sends a message through the network by writer.drain(), the message is sent to the server through handle_client. reads it and then writes it by 
sending it to the rest if client != writer(the one who sent it).
other clients receive the message from the server through receive_message(reader)

All messages must pass through the server which handles them and control the traffic
'''

# Handle the clients connection to the server
'''clients= []
async def handle_clients(reader, writer):
    addr= writer.get_extra_info('peername')
    clients.append(writer)
    #clients= {}
    #clients[writer] = {'addr': addr, 'id': client_id}

    print(f"New connection from {addr}")

    while True:
        try:
            data= await reader.read(100)
            if not data:
                break
            message= data.decode()
            writer.write('ASK'.encode())
            print(f"Received {message} from {addr}")

            for client in clients:
                if client != writer:
                    client.write(f"{addr} says {message}".encode())
                    await client.drain()
        except asyncio.CancelledError:
            pass  

    print(f"Closing connection from {addr}")
    writer.close()
    await writer.wait_closed()
    clients.remove(writer)


# Handle server
async def start_server():
    server= await asyncio.start_server(handle_clients, '127.0.0.1', 8888)
    addr= server.sockets[0].getsockname()
    print(f"Server on {addr!r}")

    async with server:
        await server.serve_forever()

# Send a message
async def send_message(writer):
    while True:
        message= input("Enter a message: ")
        writer.write(message.encode())
        await writer.drain()

# Receive a message
async def receive_message(reader):
    while True:
        data= await reader.read(1024)
        if not data:
            break
        message= data.decode()
        print(f"Message received: {message}")
    

# Handle connection
async def client_connection():
    await asyncio.sleep(2)
    reader, writer= await asyncio.open_connection('127.0.0.1', 8888)
    print("Connected to the server")
    await asyncio.gather(send_message(writer), receive_message(reader))


async def main():
    choice= input("server or client (c/s)? ")
    if choice == 's':
        await start_server()
    elif choice == 'c':
        await client_connection()

asyncio.run(main())'''

'''------------------------------------------------------------------'''


# Handle client-server communication with response from the server

# Handle connection between client and server
'''async def handle_connection(reader, writer):
    addr= writer.get_extra_info('peername')
    print(f"Connected to {addr}")
    try:
        while True:
            data= await reader.read(100)
            if not data:
                break
            message= data.decode()
            print(f"{message} received from {addr}")

            response= "Message is received"
            writer.write(response.encode())
            await writer.drain()

            if message == "exit":
                #print(f"Connection closed from {addr}")
                response= f"\nGoodbye"
                writer.write(response.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                break
            
    except asyncio.CancelledError:
        print(f"Connection with {addr} is cancelled")
    
    print(f"Connection from {addr} is closed")
    

# Start a server
async def start_server():
    server= await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    addr= server.sockets[0].getsockname()
    print(f"Server on {addr}")

    async with server:
        await server.serve_forever()



# Send messages
async def send_message(writer):
    while True:
        message= input("Write message: ")

        if message.lower() == "exit":
            print("Closing the connection")
            writer.write("exit".encode())
            await writer.drain()
            break

        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(1)

# Receive message
async def receive_message(reader):
    while True:
        data= await reader.read(100)
        if not data:
            break
        message= data.decode()
        print(f"Server: {message}")


# Connect the client socket with the server socket
async def main_connection():
    #await asyncio.sleep(2)
    reader, writer= await asyncio.open_connection('127.0.0.1', 8888)
    print("Connected to the server")
    await asyncio.gather(send_message(writer), receive_message(reader))


# Activate the server and client
async def main():
    choice= input("server or client c/s?")
    if choice == "s":
        await start_server()
    elif choice == "c":
        await main_connection()

asyncio.run(main())
'''
'''------------------------------------------------------------------------------------------------------------'''


# Handle the traffic connection for many clients
clients=[]
async def handle_traffic(reader, writer):
    addr= writer.get_extra_info('peername')
    #name= await reader.read(100)
    #username= name.decode()
    print(f"Connected to {addr[1]}")
    clients.append(writer)

    try:
        while True:
            data= await reader.read(100)
            if not data:
                break
            message= data.decode()
            print(f"{message} from {addr[1]}")

            if message != "exit":
                response= "Message received"
                writer.write(response.encode())
                await writer.drain()
                for client in clients:
                    if client != writer:
                        client.write(f"{addr[1]} says {message}".encode())
                        await client.drain()
                        

            if message == "exit":
                response= f"\nGoodbye"
                writer.write(response.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                break
            

    except asyncio.CancelledError:
        print(f"Connection is closed with {addr[1]}")

    clients.remove(writer)
    print(f"Connection is closed with {addr[1]}")
    


# start a server
async def start_server():
    server= await asyncio.start_server(handle_traffic, '127.0.0.1', 8888)
    addr= server.sockets[0].getsockname()
    print(f"Server on {addr}")

    async with server:
        await server.serve_forever()


# send a message
async def send_message(writer):
    '''name= input("Enter a username: ")
    writer.write(name.encode())
    await writer.drain()'''
    while True:
        # message= input("Write message: \n")
        ''' Here input is a synchronous function which doesn't allow any message to appear. The messages appear late from the 
            other clients bcs at the end of the loop there's a sleep for one sec which allows messages from the server to appear.
            Then this lag allows the lagged messages to pass through. 
            But allowing input to run as asynchrocnous in the background in the loop of events, will stop any lag.
        '''
        await asyncio.sleep(1)
        message= await asyncio.to_thread(input, "Write message: \n")
    
        if message.lower() == "exit":
            writer.write("exit".encode())
            await writer.drain()
            break
        
        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(1)


# Receive message
async def receive_message(reader):
    while True:
        data= await reader.read(100)
        if not data:
            break
        message= data.decode()
        print(f"{message}")


# Handle cleint connection
async def clients_connection():
    reader, writer= await asyncio.open_connection('127.0.0.1', 8888)

    print("Connected to server")
    await asyncio.gather(send_message(writer), receive_message(reader))


# Choose the service
async def main():
    choice= input("server or client c/s ")
    if choice == "s":
        await start_server()
    elif choice == "c":
        await clients_connection()

asyncio.run(main())










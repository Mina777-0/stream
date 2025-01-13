import asyncio
import socket


clients=[]
# Create a protocol
class MyProtocol(asyncio.Protocol):
    # Establish connection with a node
    def connection_made(self, transport):
        self.transport= transport
        self.client_addr= transport.get_extra_info('peername')
        print(f"Connection established with {self.client_addr}")
        clients.append(self)
        self.paused= False

    def data_received(self, data):
        message= data.decode()
        print(f"{message} received from {self.client_addr}")

        if message.lower().strip()== "exit":
            self.transport.write("Goodbye".encode())
            self.transport.close()
            for client in clients:
                if client is not self:
                    client.transport.write(f"{self.client_addr} has left".encode())
            return
        
        response= "message received"
        # To control to server buffer in case of too many connections
        if not self.paused:
            self.transport.write(response.encode())

        for client in clients:
            if client is not self:
                try:
                    client.transport.write(f"{self.client_addr} says: {message}".encode())
                except Exception as e:
                    print(f"Error sending to {client.client_addr} {e}")
                    clients.remove(client)

    def pause_writing(self):
        self.paused= True

    def resume_writing(self):
        self.paused= False

    def connection_lost(self, exc:Exception|None) -> None:
        if exc:
            print("Connection lost due to error")
        else:
            print("Connection is closed cleanly")

        if self in clients:
            clients.remove(self)

        


# Start a server
async def start_server():
    loop= asyncio.get_event_loop()

    # Set the socket
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.listen(5)
    server_socket.setblocking(False)
    print("Server started on 127.0.0.1:8000")

    server= await loop.create_server(
        lambda: MyProtocol(), sock=server_socket
    )

    server_addr= server.sockets[0].getsockname()
    print(f"Server on {server_addr}")

    async with server:
        await server.serve_forever()


# Client writes and send messages
async def send_message(writer):
    while True:
        message= await asyncio.to_thread(input, "Write your message: \n")

        if message.strip().lower() == "exit":
            writer.write(message.encode())
            await writer.drain()
            break

        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(1)

# Client receives and read messages
async def receive_message(reader):
    while True:
        data= await reader.read(100)
        if not data:
            break
        message= data.decode()
        print(f"{message}")


# Create the connection with the server
async def open_connection():
    reader, writer= await asyncio.open_connection("127.0.0.1", 8000)
    await asyncio.gather(send_message(writer), receive_message(reader))

# Run the connection
async def main():
    choice= input("Server or Client c/s? ")
    if choice == "s":
        await start_server()
    else:
        await open_connection()

asyncio.run(main())




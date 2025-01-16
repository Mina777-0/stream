import socket 
import threading

def handle_client(client_socket, addr):
    
    while True:
        try:
            # Recieve data up to 1MB
            data= client_socket.recv(1024)
            if not data:
                break

            message= data.decode('utf-8')
            print(f"{message} from {addr}")

            response= "Message is recieved"
            client_socket.sendall(response.encode('utf-8'))

            if message.lower() == "exit":
                print(f"Closing connection with {addr}")
                client_socket.close()
                break

        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()


def server_():
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    print(f"Server running on 127.0.0.1:8080")

    while True:
        client_socket, addr= server_socket.accept()
        print(f"Connected to {addr}")

        thread= threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
    

def client_():
    try:
        client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8080))
        addr= client_socket.getpeername()
        while True:
            send_msg= input("Write a message.. ")
            client_socket.sendall(send_msg.encode('utf-8'))

            if send_msg.lower() == "exit":
                client_socket.send("Good bye".encode('utf-8'))
                client_socket.close()


            data= client_socket.recv(1024)
            recv_msg= data.decode('utf-8')
            print(f"{recv_msg} from {addr}")
            

            
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()


def main():
    r= input("Client or Server c/s: ")
    if r== "c":
        client_()
    elif r == "s":
        server_()

main()
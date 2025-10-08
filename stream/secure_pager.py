import asyncio, ssl
from asyncio.streams import StreamWriter, StreamReader
from dotenv import load_dotenv
import os 

load_dotenv('demo.env')
password= os.environ.get('PASSWORD')
password_bytes= bytes(password, encoding='utf-8')
CLIENTS= []

async def handle_connection(reader: StreamReader, writer: StreamWriter):
   
    peername= writer.get_extra_info('peername')
    ssl_object= writer.get_extra_info('ssl_object')
    print(f"\nUnecrypted connection accepted with {peername}")
    print(f"\n[SERVER] protocol negotiated: {ssl_object.version()} | cipher: {ssl_object.cipher()}")
    CLIENTS.append(writer)

    try:
        while True:
            data= await reader.read(1024)
            if not data:
                break 

            message= data.decode('utf-8')
            print(f"{message} from {peername}")

            if message.lower().strip() == "exit":
                writer.write('Connection is closing ..'.encode('utf-8'))
                await writer.drain()

                for client in CLIENTS:
                    if client != writer:
                        client.write(f"Connection is closed with {peername}")
                        await client.drain()

                writer.close()
                await writer.wait_closed()
                break

            else:
                writer.write("received".encode('utf-8'))

                for client in CLIENTS:
                    if client != writer:
                        client.write(f"{peername}: {message}".encode('utf-8'))
                        await client.drain()
    except ConnectionResetError as e:
        print(f"[SERVER]:CLient {peername} disconnected unexpectedly ")
    except Exception as e:
        print(f"Unexpecte error: {e}")

    CLIENTS.remove(writer)



async def sserver():
    context= ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile='cert.pem', keyfile='key.pem', password=password_bytes)
    except FileNotFoundError:
        print(f"ERROR: 'cert.pem' or 'key.pem' is missing")
        return
    
    server= await asyncio.start_server(handle_connection, host="127.0.0.1", port=8080, ssl= context)
    
    addr= server.sockets[0].getsockname()
    print(f"[SERVER]: Secure server started on {addr}. Wait for connections ..")

    async with server:
        await server.serve_forever()


async def send_message(writer:StreamWriter):
    while True:
        messsage= await asyncio.to_thread(input, "Message: ")

        if messsage.lower().strip() == "exit":
            writer.write('exit'.encode('utf-8'))
            await writer.drain()
            break

        writer.write(messsage.encode('utf-8'))
        await writer.drain()
        await asyncio.sleep(1)

async def read_message(reader: StreamReader):
    while True:
        data= await reader.read(2048)
        if not data:
            break
        message= data.decode('utf-8')
        print(message)


async def client_connection():
    context= ssl.create_default_context()
    context.check_hostname= False
    context.verify_mode= ssl.CERT_REQUIRED

    try:
        context.load_verify_locations('cert.pem')
    except FileNotFoundError:
        print(f"ERROR: 'cert.pem' is missing")
        return

    try:
        reader, writer= await asyncio.open_connection(
            host="127.0.0.1",
            port=8080,
            ssl=context,
            server_hostname= "127.0.0.1"
        )

        server_addr= writer.get_extra_info('peername')
        ssl_object= writer.get_extra_info('ssl_object')
        print(f"\n[CLIENT]: Secured connection established with server {server_addr}")
        print(f"\n[ClIENT]: Protocol negotiated: {ssl_object.version()} | cipher: {ssl_object.cipher()}")
        

        await asyncio.gather(send_message(writer), read_message(reader))

    except ConnectionResetError:
        print(f"[CLIENT ERROR]: Connection refused. Is the server running? ")
    except ssl.SSLCertVerificationError as e:
        print(f"[CLIENT ERROR]: Certificate verification failed: {e}")
    except Exception as e:
        print(f"[CLIENT ERROR]: {e}")
    finally:
        if writer and not writer.is_closing():
            writer.close()
            await writer.wait_closed()

    
async def main():
    service= input("What's the service s/c? ")
    if service == "s":
        await sserver()
    else:
        await client_connection()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programme stopped by user")


from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timezone, timedelta
import ipaddress
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os


load_dotenv('demo.env')


def generate_password_key():
    key= Fernet.generate_key()
    if not os.path.exists('demo.env'):
        print("'demo.env' doesn't exist")
    else:
        print("'demo.env' exists")

    
    with open('demo.env', 'w') as f:
        f.write(f"PASSWORD={key.decode('utf-8')}")
            
    print(key)           

#generate_password_key()


#password= os.environ.get('PASSWORD')
#password_bytes= bytes(password, encoding='utf-8')

def generate_cert_and_key(host_ip):
    private_key= rsa.generate_private_key(
        public_exponent=65537,
        key_size= 2048
    )

    subject= issuer= x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'AE'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'Local'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'Local'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Secured layer'),
        x509.NameAttribute(NameOID.COMMON_NAME, host_ip)
    ])

    ip_address= ipaddress.ip_address(host_ip)

    cert= (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ip_address)]), critical= False)
        .sign(
            private_key,
            hashes.SHA256(),
            default_backend()
        )
    )

    with open('key.pem', 'wb') as f:
        f.write(
            private_key.private_bytes(
                encoding= serialization.Encoding.PEM,
                format= serialization.PrivateFormat.PKCS8,
                encryption_algorithm= serialization.BestAvailableEncryption(password_bytes)
            )
        )

    with open('cert.pem', 'wb') as f:
        f.write(
            cert.public_bytes(
                encoding= serialization.Encoding.PEM
            )
        )

#generate_cert_and_key("127.0.0.1")



    

import asyncio
import time

# Asynchronous functions can't be called like synchronous functions. we have to use asyncio.run() 

'''async def main():
    print("hello")
    await asyncio.sleep(10)
    print("Bye")

asyncio.run(main())



async def say_after(delay, say):
    await asyncio.sleep(delay=delay)
    print(say)

async def main():
    print(f"Started at {time.strftime('%X')}")
    await say_after(3, "hello")
    print(f"Finished at {time.strftime('%X')}")

asyncio.run(main())

''' 


# asyncio.create_task()
'''async def say_after(delay, say):
    await asyncio.sleep(delay=delay)
    print(say)


async def main():
    
    When you use create_task(), it immediately schedules the say_after(3, "hello") coroutine to run in the background, 
    allowing other parts of the code (including other asynchronous tasks) to continue running without waiting for task1 to finish.
    It doesn't block the execution of the next line of code in main().
    
    task1= asyncio.create_task(say_after(3, "hello"))

    
    say_after(6, "bye") is called directly, returning a coroutine object. However, this coroutine will only start execution when 
    you explicitly await it. In other words, this function is not scheduled as a task in the event loop until it is awaited. 
    The coroutine is not running concurrently with the rest of the code; the execution will pause when the code reaches await task2.
    task2 is not running concurrently. It will only start when you hit the await task2 line after task1 finishes.
    
    task2= say_after(6, "bye")
    #task2= asyncio.create_task(say_after(6, "bye"))

    print(f"start at {time.strftime('%X')}")

    await task1
    await task2

    print(f"finish at {time.strftime('%X')}")

asyncio.run(main())'''

# Output:
'''
task1 starts running immediately in the background.
The say_after(6, "bye") coroutine (assigned to task2) won't start until the program reaches await task2.
The await task1 ensures that the program waits for task1 to complete (which takes 3 seconds).
After task1 finishes, task2 is awaited, starting the 6-second delay for the second message.
The total runtime will be 9 seconds (3 seconds for task1 and 6 seconds for task2), as the tasks run sequentially, not concurrently.

If both were added to the loop event, they'd have run in the background without any delay. The total time here would be 6 seconds.
The time of the longer period


start at 16:24:05
hello
bye
finish at 16:24:14
9 seconds difference

start at 16:40:53
hello
bye
finish at 16:40:59
6 seconds difference
'''



# Event loops 

'''
The event loop is indeed the heart of the asyncio library in Python. It orchestrates the execution of asynchronous tasks, 
handles IO operations, and schedules events. Understanding how it works and how to interact with it can give you powerful control 
over your application's behavior, especially when working with low-level code or creating custom frameworks.

Breaking It Down:
Role of the Event Loop:
* Task Execution: The event loop schedules and runs async tasks (coroutines) and callbacks. It ensures these tasks are run in an 
interleaved manner, creating the illusion of concurrency.
* Non-blocking IO: It handles socket operations, file reads/writes, and other IO in a non-blocking way, allowing your application to 
remain responsive while waiting for external resources.
* Event Scheduling: You can schedule functions or callbacks to run after a certain delay or at regular intervals.


The event loop in asyncio is not a simple data structure like a dictionary or list. Instead, it is an object provided by the 
asyncio library. This object encapsulates complex logic for managing asynchronous tasks, callbacks, and events.

What Is an Event Loop in Python?
Type: It is an instance of a class, typically asyncio.BaseEventLoop or its subclass asyncio.AbstractEventLoop.
Purpose: The event loop is the core engine that manages when and how asynchronous operations are executed.


How Does the Event Loop Work Internally?
At its core, the event loop:

Maintains Queues:

It keeps track of pending tasks, callbacks, and events in various internal data structures like queues or priority heaps.
For example:
A queue of tasks waiting to be executed.
A queue of timers for scheduling callbacks at specific times.
Iterates Continuously:

The event loop continuously runs, checking these queues, processing tasks, and moving between different states like waiting for IO or handling timeouts.
This iteration is where the "loop" concept comes in—it cycles through tasks repeatedly.
Relies on System Calls:

It uses low-level operating system features (e.g., epoll on Linux, kqueue on macOS, or Select on Windows) to monitor IO events efficiently.

CALLBACK functions vs ASYNCHRONOUS functions
A callback function is a traditional function that gets called when an asynchronous operation completes, or when a certain event occurs.

import asyncio

def callback_function(future):
    # This runs *after* the async operation is complete
    result = future.result()  # Get the result of the async function
    print(f"Callback: The result is {result}")

async def async_function():
    print("Async operation started")
    await asyncio.sleep(2)  # Simulates a delay (asynchronous operation)
    print("Async operation completed")
    return "Data from async_function"

async def main():
    future = asyncio.ensure_future(async_function())  # Schedule async_function
    future.add_done_callback(callback_function)  # Attach the callback
    await future  # Wait for async_function to complete

asyncio.run(main())


# Coroutines

import asyncio

async def greet(name):
    print(f"Hello, {name}!")
    await asyncio.sleep(1)
    print(f"Goodbye, {name}!")

async def main():
    await greet("Alice")
    await greet("Bob")

asyncio.run(main())

Hello, Alice!
Goodbye, Alice!
Hello, Bob!
Goodbye, Bob!


# Callback 

import asyncio

def greet_callback(future, name):
    try:
        future.result()  # To propagate any exceptions
        print(f"Goodbye, {name}!")
    except Exception as e:
        print(f"Error: {e}")

async def greet(name):
    print(f"Hello, {name}!")
    await asyncio.sleep(1)

async def main():
    future = asyncio.ensure_future(greet("Alice"))
    future.add_done_callback(lambda fut: greet_callback(fut, "Alice"))
    
    future2 = asyncio.ensure_future(greet("Bob"))
    future2.add_done_callback(lambda fut: greet_callback(fut, "Bob"))
    
    await asyncio.gather(future, future2)

asyncio.run(main())


Hello, Alice!
Hello, Bob!
Goodbye, Alice!
Goodbye, Bob!


'''

'''async def greet():
    print("hello")
    await asyncio.sleep(2)
    print("Goodbye")

loop= asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(greet())
finally:
    loop.close()'''


# Customise protocols using asyncio.protocol

'''
The "buffer" in the context of asyncio.Protocol refers to the transport's internal write buffer, which temporarily holds data before it's sent over 
the network. If too much data is written too quickly, the buffer might become full, which can lead to performance issues or memory pressure.

Why Use Such a Large Response?
To Simulate Large Data Transfers:

This example creates a scenario where the server is trying to send a large amount of data to the client.
It mimics a high-bandwidth server or one that streams large responses (e.g., file downloads or logs).
To Test Flow Control:

Sending a large response can fill up the transport’s write buffer.
This tests whether pause_writing() and resume_writing() handle backpressure correctly.
To Observe Buffer Behavior:

You can monitor how the server manages the buffer and ensure it doesn't overwhelm itself or the client.

class MyProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport= transport
        client_addr= transport.get_extra_info('peername')
        print(f"Connectin established with {client_addr}")
        self.paused= False

    def data_received(self, data):
        print(f"Data received {data.decode()}")
        # Simulates large response
        response= "Data received\n" * 10000 
        # Echo to the client
        if not self.paused:
            self.transport.write(response.encode())

    def pause_writing(self):
        self.paused= True

    def resume_writing(self):
        self.paused= False

    def connection_lost(self, exc: Exception | None) -> None:
        if exc:
            print("Connection lost due to error")
        else:
            print("Connection closed cleanly")
    

async def create_server():
    loop= asyncio.get_running_loop()
    server= await loop.create_server(
        protocol_factory=MyProtocol,
        host="0.0.0.0",
        port=8888,
        reuse_address=True,
        reuse_port=True
    )
    addr= server.sockets[0].getsockname()
    print(f"Server is connected on {addr}")
    async with server:
        await server.serve_forever()

asyncio.run(create_server())


# Start a server
async def start_server():
    loop= asyncio.get_event_loop()
    # Determine the ipv and the protocol type: TCP
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    This specifies that the option is a socket-level option. There are other levels 
    (e.g., IPPROTO_TCP for TCP-specific options), but SOL_SOCKET is for general socket options.
    Tell the operating system to reuse the address in case of closed connection. If the socket is connected to a port and closed,
    it'll take short time to reconnect again. By this, it'll connect automatically
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind("127.0.0.1", 8000)
    
    The operating system will listen to new connections
    When a client initiates a connection to the server, the OS places the connection in a queue.
    This queue is maintained by the OS until your server application explicitly accepts the connection using accept() 
    (or await loop.sock_accept() in asyncio).
    The backlog value (5 in this case) limits the size of the connection queue.
    If the queue is full (i.e., more than 5 connections are waiting), the OS rejects additional connection attempts 
    (usually with an error like ECONNREFUSED).
    If the queue has fewer than 5 pending connections, the OS adds the new connection to the queue, and the client waits for 
    your server to accept() it.
    If the queue already has 5 pending connections, the OS rejects the new connection attempt.
    For example, even with listen(5), you could have 1000 active connections as long as your application is fast enough to accept 
    them before the queue fills.
    
    server_socket.listen(5)
    
    False: When set to False, the socket becomes non-blocking. This means operations like accept(), recv(), and send() will return 
    immediately, even if no data is available or no connection is pending. The application will need to handle the potential lack of 
    data or connections by checking for availability (e.g., using asyncio or select).
    Why use non-blocking?: In asynchronous programming, non-blocking sockets are important because they allow your program to continue 
    executing while waiting for network events (like data arrival or new connections) without getting "stuck" waiting for those events.
    Setting non-blocking mode: You set the socket to non-blocking mode, allowing asynchronous handling of connections without blocking 
    the rest of the program.
    
    server_socket.setblocking(False)
    print("Server started on 127.0.0.1:8000")

    server= await loop.create_server(
        lambda: MyProtocol(), sock=server_socket
    )

    async with server:
        server.serve_forever()
'''

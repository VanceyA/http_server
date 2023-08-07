import socket
import sys
import os

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# listen on the port
server_addr = 'localhost'
server_port = 80
if len(sys.argv) > 1:
    try:
        server_port = int(sys.argv[1])
    except ValueError:
        print("Invalid port")
        sys.exit(1)
s.bind((server_addr, server_port))
s.listen(1)
print("Server running on", server_addr, "port", server_port)

while True:
    try:
        # accept a new connection
        client_s, client_addr = s.accept()

        # wait for request
        msg = client_s.recv(2048)
        print("Received:", msg.decode('ascii'))
        msg_str = msg.decode()
        fname = msg_str.split(" ")[1]
        fname = fname[1:]
        
        try:
            with open(fname, 'r') as f:
                message = f.read()
            # send response
            message = f'HTTP/1.1 200 OK\r\nContent-Length: {len(message)}\r\nContent-Type: text/html\r\n{message}'
            client_s.send(message.encode('ascii'))
        except FileNotFoundError:
            header = 'HTTP/1.1 404 Not Found\nContent-Length: 23\nContent-Type: text/html\r\n'
            response = header.encode('ascii') + b'404 Not Found\n'
            client_s.send(response)
    
    except KeyboardInterrupt:
        break
    finally:
        client_s.close()
s.close()
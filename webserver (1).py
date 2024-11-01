import socket

print('Starting Python webserver...')
sock = socket.socket()
sock.bind(('0.0.0.0', 14000))
print('Binding to port 14000 complete.')
print('Starting to listen...')
sock.listen()

while True:
    # Accept connection
    conn, addr = sock.accept()
    print('Connection accepted from:', addr)
    
    # Receive request
    msg = conn.recv(2048)
    request = msg.decode()
    print('Request received:', request)
    
    # Parse request
    tokens = request.split()
    if len(tokens) < 2:
        continue  # Invalid request, continue listening
    
    cmd = tokens[0]
    target_file = tokens[1]

    # Map requested file to actual file
    file_mapping = {
        '/index.html': 'index.html',
        '/alien.html': 'alien.html',
        '/human.html': 'human.html'
    }

    
    if cmd == 'GET' and target_file in file_mapping:
        try:
            # Open and read requested file
            with open(file_mapping[target_file], 'r') as f:
                file_contents = f.read()

            # Send response
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html\r\n\r\n'
            response += file_contents
            conn.sendall(response.encode())
        except FileNotFoundError:
            
            response = 'HTTP/1.1 404 Not Found\r\n'
            response += 'Content-Type: text/html\r\n\r\n'
            response += '<h1>404 Not Found</h1>'
            conn.sendall(response.encode())
    else:
        
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += 'Content-Type: text/html\r\n\r\n'
        response += '<h1>404 Not Found</h1>'
        conn.sendall(response.encode())

    # Close connection
    conn.close()

sock.close()
print('Python webserver complete')

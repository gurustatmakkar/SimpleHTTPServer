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
        '/human.html': 'human.html',
        '/image.jpg': 'image.jpg'  # Add support for serving image.jpg
    }

    if cmd == 'GET' and target_file in file_mapping:
        try:
            # Open and read requested file
            with open(file_mapping[target_file], 'rb') as f:  # Open in binary mode for images
                file_contents = f.read()

            # Determine content type based on file extension
            if target_file.endswith('.html'):
                content_type = 'text/html'
            elif target_file.endswith('.jpg'):
                content_type = 'image/jpeg'

            # Send response
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: {}\r\n\r\n'.format(content_type)
            response_binary = response.encode() + file_contents
            conn.sendall(response_binary)
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


import socket

# Create a TCP/IP socket
proxy_socket = socket.socket()

# Bind the socket to the port
proxy_socket.bind(('0.0.0.0', 14001))

# Listen for incoming connections
proxy_socket.listen()

print('Proxy server is listening on port 14001...')

while True:
    # Wait for a connection
    client_conn, client_addr = proxy_socket.accept()
    print('Connection accepted from:', client_addr)

    # Receive the request from the client
    request = client_conn.recv(1024).decode()
    print('REQUEST: ', request)

    # Parse the requested URL
    url_parts = request.split()
    if len(url_parts) > 1:
      target_host = url_parts[1][1:]
    else: 
      print('bogus request, continuing')
      client_conn.close()
    target_port = 80
    if target_host:
        print("Target host: ",target_host)
    else:
        print("Target error")
        client_conn.close()
        continue
        

    # Create a socket to communicate with the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(' Trying to connect')
    target_socket.connect((target_host, target_port))

    # Send the request to the target server
    print('sending request to target')
    target_socket.sendall('GET / HTTP/1.0\r\n'.encode())
    x = 'Host: ' + target_host + '\r\n\r\n'
    target_socket.sendall(x.encode())   
    print('request sent to target')
    # Receive the response from the target server

    print('waiting for target response')  
    data = target_socket.recv(1024)
    print('target response received: ', data.decode())
    print('forwarding to client')
    # Send the response back to the client
    client_conn.sendall(data)
    print('data sent to client')
    # Close the connections
    target_socket.close()
    client_conn.close()
    print('sockets closed, going back to while')

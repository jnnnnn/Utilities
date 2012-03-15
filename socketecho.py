import socket
addr, port = 'localhost', 9001
s = socket.socket()
s.bind(('localhost', 9001))
s.listen(0)
print("Listening for connections on %s:%d"%(addr, port))
conn, address = s.accept()
print("Connected.")
while 1:
    data = conn.recv(4096)
    if not data: break
    print(data)
conn.close()
print("Connection closed.")

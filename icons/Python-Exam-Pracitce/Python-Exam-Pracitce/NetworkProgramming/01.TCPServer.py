import socket
s = socket.socket()
host = socket.gethostname()
port = 9999
s.bind((host, port))
print("Waiting for connection!")
s.listen(5)
msg = "Saying hiee!"

while True:
    conn, addr = s.accept()
    print("Got connecion from", addr)
    conn.send(msg.encode()) 
    conn.close()
import socket

HOST = "127.0.0.1"
PORT = 6000

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Legacy B waiting...")
conn, _ = server.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break

    print("Received:", data.decode())
    reply = input("Reply: ")
    conn.send(reply.encode())

conn.close()
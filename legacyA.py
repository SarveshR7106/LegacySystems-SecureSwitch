import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to Secure Switch A")

while True:
    msg = input("Send: ")
    if msg.lower() == "exit":
        break

    client.send(msg.encode())
    reply = client.recv(1024)
    print("Reply:", reply.decode())

client.close()
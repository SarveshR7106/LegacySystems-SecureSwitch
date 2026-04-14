import requests
import socket
import threading
from Cryptodome.Cipher import AES
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

PC2_IP = "172.16.97.4"

def send_log(data):
    try:
        requests.post(f"http://{PC2_IP}:8000/log", json=data)
    except:
        pass

def perform_key_exchange(sock):
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    peer_pub = sock.recv(1024)

    sock.send(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    peer_key = serialization.load_pem_public_key(peer_pub)

    shared = private_key.exchange(ec.ECDH(), peer_key)

    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'secure'
    ).derive(shared)

def decrypt_send(tunnel, legacy, key):
    while True:
        packet = tunnel.recv(1024)
        if not packet:
            break

        nonce = packet[:16]
        tag = packet[16:32]
        ct = packet[32:]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        data = cipher.decrypt_and_verify(ct, tag)

        print("[B] Encrypted:", ct.hex())
        print("[B] Decrypted:", data.decode())

        send_log({
            "type": "B",
            "ciphertext": ct.hex(),
            "decrypted": data.decode()
        })

        legacy.send(data)

def encrypt_send(legacy, tunnel, key):
    while True:
        data = legacy.recv(1024)
        if not data:
            break

        cipher = AES.new(key, AES.MODE_GCM)
        ct, tag = cipher.encrypt_and_digest(data)

        packet = cipher.nonce + tag + ct
        tunnel.send(packet)

server = socket.socket()
server.bind(("0.0.0.0", 7000))
server.listen(1)

print("Switch B waiting...")
tunnel, _ = server.accept()

key = perform_key_exchange(tunnel)

legacy = socket.socket()
legacy.connect(("127.0.0.1", 6000))

threading.Thread(target=decrypt_send, args=(tunnel, legacy, key)).start()
threading.Thread(target=encrypt_send, args=(legacy, tunnel, key)).start()
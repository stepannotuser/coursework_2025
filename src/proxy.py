# proxy.py
import socket
from threading import Thread
from datetime import datetime

LISTEN_PORT = 9101
SERVER_ADDR = ('127.0.0.1', 9100)
LOG_FILE = 'proxy_log.txt'

def log(msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg.strip() + '\n')

def handle(client_sock):
    with client_sock, socket.create_connection(SERVER_ADDR) as server_sock:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            log(msg)
            server_sock.sendall((msg + '\n').encode())

            response = b''
            while not response.endswith(b'\n'):
                chunk = server_sock.recv(1024)
                if not chunk: break
                response += chunk
            client_sock.sendall(response)

def run_proxy():
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', LISTEN_PORT))
        s.listen()
        print(f'[proxy] listening on port {LISTEN_PORT}')
        while True:
            client_sock, _ = s.accept()
            Thread(target=handle, args=(client_sock,), daemon=True).start()

if __name__ == '__main__':
    run_proxy()

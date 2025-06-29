import socket, threading, sys
from contextlib import closing

class TurnstileFSM:
    def __init__(self):
        self.state = 'LOCKED'
    def step(self, inp: str) -> str:
        s = self.state
        if s == 'LOCKED':
            if inp == 'coin':  self.state = 'UNLOCKED'; return 'unlock'
            if inp == 'push':  return 'alarm'
        elif s == 'UNLOCKED':
            if inp == 'push':  self.state = 'LOCKED';   return 'pass'
            if inp == 'coin':  return 'thank'
        return 'invalid'

def serve(host='127.0.0.1', port=9100):
    with closing(socket.socket()) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen()
        print(f"[turnstile] listening on {host}:{port}")
        while True:
            conn, _ = srv.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

def handle(conn: socket.socket):
    fsm, buf = TurnstileFSM(), b''
    with conn:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            buf += chunk
            while b'\n' in buf:
                line, buf = buf.split(b'\n', 1)
                out = fsm.step(line.decode().strip())
                conn.sendall((out + '\n').encode())

if __name__ == '__main__':
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 9100
    serve(port=p)

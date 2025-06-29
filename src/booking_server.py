# booking_server.py
import socket, threading, sys
from contextlib import closing

class BookingFSM:
    def __init__(self):
        self.state = 'IDLE'
    def step(self, inp: str) -> str:
        parts = inp.strip().split()
        cmd = parts[0] if parts else ''
        if self.state == 'IDLE':
            if cmd == 'login': self.state = 'AUTHED'; return 'Welcome'
            return 'Login first'
        elif self.state == 'AUTHED':
            if cmd == 'select': self.state = 'SELECTING'; return 'Seat selected'
            if cmd == 'logout': self.state = 'IDLE'; return 'Goodbye'
        elif self.state == 'SELECTING':
            if cmd == 'confirm': self.state = 'BOOKED'; return 'Ticket booked'
            if cmd == 'cancel': self.state = 'CANCELLED'; return 'Booking canceled'
        elif self.state == 'BOOKED':
            if cmd == 'cancel': self.state = 'CANCELLED'; return 'Booking canceled'
        if cmd == 'logout':
            self.state = 'IDLE'; return 'Goodbye'
        return 'Invalid'

def serve(host='127.0.0.1', port=9100):
    with closing(socket.socket()) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen()
        print(f"[booking_server] listening on {host}:{port}")
        while True:
            conn, _ = srv.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

def handle(conn: socket.socket):
    fsm, buf = BookingFSM(), b''
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

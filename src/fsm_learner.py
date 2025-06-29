#https://github.com/DES-Lab/AALpy

import socket, sys, importlib, inspect, json, argparse
from aalpy.base import SUL

#https://github.com/DES-Lab/AALpy/blob/master/aalpy/base/SUL.py

class SocketSUL(SUL):
    def __init__(self, host, port):
        super().__init__()
        self.host, self.port = host, port
        self.sock = None
    def pre(self):
        self.sock = socket.create_connection((self.host, self.port))
    def post(self):
        if self.sock:
            self.sock.close()
    def step(self, letter):
        self.sock.sendall((letter + '\n').encode())
        data = b''
        while not data.endswith(b'\n'):
            chunk = self.sock.recv(1024)
            if not chunk: raise ConnectionError('server closed')
            data += chunk
        return data.decode().strip()

try:
    from aalpy.learning_algs import run_Lstar_mealy
except ImportError:
    base = importlib.import_module('aalpy.learning_algs').run_Lstar

#https://github.com/DES-Lab/AALpy/blob/master/aalpy/learning_algs/deterministic/LStar.py

    def run_Lstar_mealy(alpha, sul, eq_oracle, print_level=2):
        return base(alpha, sul, eq_oracle,
                    automaton_type='mealy', print_level=print_level)

#https://github.com/DES-Lab/AALpy/blob/master/aalpy/oracles/RandomWordEqOracle.py
#

from aalpy.oracles import RandomWMethodEqOracle, RandomWordEqOracle
def make_eq(alpha, sul):
    try:
        sig = inspect.signature(RandomWMethodEqOracle).parameters
        kwargs = {'walk_len': 25, 'reset_prob': .5}
        if 'walks'          in sig: kwargs['walks']           = 500
        elif 'num_walks'    in sig: kwargs['num_walks']       = 500
        elif 'walks_per_state' in sig: kwargs['walks_per_state'] = 20
        else: raise ValueError
        return RandomWMethodEqOracle(alpha, sul, **kwargs)
    except Exception:   # fallback
        return RandomWordEqOracle(alpha, sul,
                                  num_walks=8000,
                                  min_walk_len=1,
                                  max_walk_len=12,
                                  reset_after_cex=True)

def learn(host: str, port: int, alphabet: list[str]):
    sul = SocketSUL(host, port)
    eq = make_eq(alphabet, sul)
    model = run_Lstar_mealy(alphabet, sul, eq, print_level=2)

    model.visualize('learned_model.pdf')
    model.save('learned_model.dot', file_type='dot')
    print('[learner] model learned_model.dot / .json')

    return model

if __name__ == '__main__':
    input_str = argparse.ArgumentParser(description="Active learner for Mealy FSM")
    input_str.add_argument('host', nargs='?', default='127.0.0.1')
    input_str.add_argument('port', nargs='?', type=int, default=9000)
    input_str.add_argument('-a', '--alphabet', metavar='SYM', nargs='+',
                        help="list of input symbols ")
    args = input_str.parse_args()

    if not args.alphabet:
        try:
            with open('alphabet.txt', encoding='utf-8') as f:
                args.alphabet = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("error: File not found.")
            sys.exit(1)


    learn(args.host, args.port, args.alphabet)

#!/usr/bin/python3
# Filename Client3.py

import socket, sys, os, select, socketserver, struct, time, json, random
from secret3 import Secret

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass

class ClientServer(socketserver.StreamRequestHandler):
    def handle(self):
        random.seed();
        pos = random.randrange(4096)
        self.secret_in = Secret(pos)
        self.secret_out = Secret(pos)
        enc = self.secret_in.enc
        dec = self.secret_out.dec
        remote = None
        try:
            sock = self.connection
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((server_host, server_port))
            print('connected to server: ' + server_host + ":" + str(server_port))
            # send the random pos as first two bytes
            remote.send(struct.pack('>H', pos))
            # proxy the in/out streams
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])
                if sock in r:
                    if remote.send(enc(sock.recv(4096))) <= 0: break
                if remote in r:
                    if sock.send(dec(remote.recv(4096))) <= 0: break
        except socket.error:
            pass
        except IndexError:
            pass
        finally:
            if remote != None: remote.close()

def main():
    global conf, server_host, server_port, client_port
    if not os.path.exists('secret.key'):
        print('No secret.key file found, see readme.md for instruction.')
        print('Program exit.')
        sys.exit(0)
    with open('config.json', 'r') as conf_file:
        conf = json.load(conf_file)
    server_host = conf['server_host']
    server_port = conf['server_port']
    client_port = conf['client_port']
    print('config server_host: ' + server_host)
    print('config server_port: ' + str(server_port))
    print('config client_port: ' + str(client_port))
    server = ThreadingTCPServer(('', client_port), ClientServer)
    print('bind port: %d' % client_port + ' ok!')
    try:
        server.serve_forever()
    except:
        print('Interruted, exit program.')
        os._exit(1)

if __name__ == '__main__':
    main()

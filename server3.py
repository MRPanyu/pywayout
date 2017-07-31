#!/usr/bin/python3
# Filename Server3.py

import socket, sys, os, select, socketserver, struct, time, json
from secret3 import Secret

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass

class Socks5Server(socketserver.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        enc = self.secret_in.enc
        dec = self.secret_out.dec
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                if remote.send(dec(sock.recv(4096))) <= 0: break
            if remote in r:
                if sock.send(enc(remote.recv(4096))) <= 0: break
    def handle(self):
        try:
            sock = self.connection
            # read first two bytes as random pos
            data = self.rfile.read(2)
            pos = struct.unpack('>H', data)[0]
            self.secret_in = Secret(pos)
            self.secret_out = Secret(pos)
            enc = self.secret_in.enc
            dec = self.secret_out.dec
            # 1. Version/Method
            data = dec(self.rfile.read(2))
            ver = data[0]
            data = dec(self.rfile.read(data[1]))
            sock.send(enc(b'\x05\x00'));
            # 2. Request
            data = dec(self.rfile.read(4))
            mode = data[1]
            addrtype = data[3]
            addr = None
            if addrtype == 1:       # IPv4
                addr = socket.inet_ntoa(dec(self.rfile.read(4)))
            elif addrtype == 3:     # Domain name
                addr = dec(self.rfile.read(dec(self.rfile.read(1))[0]))
            addr = str(addr, 'UTF-8')
            port = struct.unpack('>H', dec(self.rfile.read(2)))
            print("addrtype: " + str(addrtype) + ", addr: " + addr + ", port: " + str(port[0]))
            reply = b'\x05\x00\x00\x01'
            try:
                if mode == 1 and addr != None:  # 1. Tcp connect
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    pass
                else:
                    reply = b'\x05\x07\x00\x01' # Command not supported
                local = remote.getsockname()
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
            except socket.error:
                # Connection refused
                reply = b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            sock.send(enc(reply))
            # 3. Transfering
            if reply[1] == 0:  # Success
                if mode == 1:    # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            pass
        except IndexError:
            pass

def main():
    global conf, server_port
    if not os.path.exists('secret.key'):
        print('No secret.key file found, see readme.md for instruction.')
        print('Program exit.')
        sys.exit(0)
    with open('config.json', 'r') as conf_file:
        conf = json.load(conf_file)
    server_port = conf['server_port']
    print('config server_port: ' + str(server_port))
    server = ThreadingTCPServer(('', server_port), Socks5Server)
    print('bind port: %d' % server_port + ' ok!')
    try:
        server.serve_forever()
    except:
        print('Interruted, exit program.')
        os._exit(1)

if __name__ == '__main__':
    main()

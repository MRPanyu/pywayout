#!/usr/bin/python3

import sys, os, random

class Secret:
    def __init__(self, pos=0):
        with open('secret.key', 'rb') as f:
            self.key = f.read()
        self.pos = pos
    def enc_byte(self, b):
        a = b + self.key[self.pos % len(self.key)]
        if a >= 256: a = a - 256
        self.pos = self.pos + 1
        return a
    def dec_byte(self, b):
        a = b - self.key[self.pos % len(self.key)]
        if a < 0: a = a + 256
        self.pos = self.pos + 1
        return a
    def enc(self, data):
        return bytes(map(self.enc_byte, data))
    def dec(self, data):
        return bytes(map(self.dec_byte, data))

# Generates a secret.key file
def gensecretkey():
    random.seed()
    barr = bytearray(4096)
    for i in range(len(barr)):
        barr[i] = random.randrange(256)
    with open('secret.key', 'wb') as f:
        f.write(barr)

# If main try generating new secret.key file
if '__main__' == __name__:
    if os.path.exists('secret.key'):
        s = input('Do you want to generate new secret.key file (Y/N)? ')
        if 'Y' != s.upper():
            sys.exit(0)
    print('Generating secret.key...')
    gensecretkey()
    print('Done.')

#!/usr/bin/python3

import sys, os, random

class Secret:
    key = None
    def __init__(self, pos=0):
        self.pos = pos % len(self.key)
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

# Secret class variable initialize
if os.path.exists('secret.key'):
    with open('secret.key', 'rb') as f:
        Secret.key = f.read()

# Generates a secret.key file
def gensecretkey(keylen):
    random.seed()
    barr = bytearray(keylen)
    for i in range(keylen):
        barr[i] = random.randrange(256)
    with open('secret.key', 'wb') as f:
        f.write(barr)

# If main try generating new secret.key file
if '__main__' == __name__:
    keylen = 4096 # default key length
    if len(sys.argv) > 1:
        keylen = int(sys.argv[1])
    if keylen < 16 or keylen > 65535: raise RuntimeError('Key length should be an integer between 16 and 65535.')
    if os.path.exists('secret.key'):
        s = input('Overwrite exist secret.key file (Y/N)? ')
        if 'Y' != s.upper():
            sys.exit(0)
    print('Generating secret.key...')
    gensecretkey(keylen)
    print('Done.')

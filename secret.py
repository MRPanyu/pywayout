#!/usr/bin/python

import sys, os, random

class Secret:
    def __init__(self, pos=0):
        with open('secret.key', 'rb') as f:
            self.key = f.read()
        self.pos = pos
    def enc_char(self, c):
        a = ord(c) + ord(self.key[self.pos % len(self.key)])
        if a >= 256: a = a - 256
        self.pos = self.pos + 1
        return chr(a)
    def dec_char(self, c):
        a = ord(c) - ord(self.key[self.pos % len(self.key)])
        if a < 0: a = a + 256
        self.pos = self.pos + 1
        return chr(a)
    def enc(self, str):
        return ''.join(map(self.enc_char, str))
    def dec(self, str):
        return ''.join(map(self.dec_char, str))
    def reset(self):
        self.pos = 0

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
    if os.path.exists("secret.key"):
        s = raw_input('Do you want to generate new secret.key file (Y/N)? ')
        if 'Y' != s.upper():
            sys.exit(0)
    print('Generating secret.key...')
    gensecretkey()
    print('Done.')

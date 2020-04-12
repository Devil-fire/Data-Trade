import os, sys
import binascii
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJECT_DIR)

from AlgoIfce import PRES
from Mine.Entity import *
from random import randint
import _pysha3


class MyScheme(PRES):

    def __init__(self):
        self.g = bn.G1
        self.h = bn.G2
        self.Z = bn.pairing(self.h, self.g)  # Z=e(g,h)
        self.bitlen = 128

    def genRandNumber(self):
        return randint(0, 2 ** self.bitlen)

    def strEncode(self, string: str):
        return int(binascii.hexlify(string.encode()), 16)

    def decodeStr(self, number: int):
        return binascii.unhexlify(hex(number)[2:].encode()).decode()

    def hashtoG2point(self, w: str):
        return bn.multiply(self.h, self.strEncode(w))

    def hashfromCipherII(self, cipherii: CipherII):
        sum = 0
        for i in cipherii.c3.coeffs:
            sum = (sum + int(i)) % (2 ** 256)
        mystring = str(sum)
        s = _pysha3.keccak_256(mystring.encode('ascii')).hexdigest()
        return int(s, 16)

    def modInverse(self, a, m):
        if self.gcd(a, m) != 1:
            return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def KeyGen(self):
        sk = self.genRandNumber()
        prikey = PriKey(sk)
        key = Key(prikey)
        return key

    def Enc(self, pubkey: PubKey, message: str, keyword: str):
        s = self.genRandNumber()
        beta = self.genRandNumber()
        c1 = bn.multiply(pubkey.pk, beta)  # g^{a\beta}
        c2 = bn.multiply(self.hashtoG2point(keyword), beta)  # H(w)^{\beta}
        c3 = self.strEncode(message) * \
             bn.pairing(self.hashtoG2point(keyword), self.g) ** (s * beta)  # m*e(H(w),g)^{s\beta}
        cipherii = CipherII(c1, c2, c3)
        srecord = Srecord(s, self.hashfromCipherII(cipherii))
        return cipherii, srecord

    def Trapdoor(self, prikey: PriKey, keyword: str):
        hw = self.hashtoG2point(keyword)
        Tw = TrapKey(bn.multiply(hw, prikey.sk))
        return Tw

    def ReKeyGen(self, pubkeyB: PubKey, prikeyA: PriKey):
        """ rekey from A to B"""
        rk = ReKey(bn.multiply(pubkeyB.pk, prikeyA.sk))
        return rk

    def Search(self, cipherii: CipherII, Tw: TrapKey, rk: ReKey):
        return bn.pairing(Tw.tk, cipherii.c1) == bn.pairing(cipherii.c2, rk.rk)

    def TokenGen(self, prikey: PriKey, sid: int, Tw: TrapKey):
        div = self.modInverse(prikey.sk, bn.curve_order)
        return Token(bn.multiply(Tw.tk, sid * div))

    def ReEnc(self, cipherii: CipherII, rk: ReKey, tk: Token):
        r = self.genRandNumber()
        c1 = bn.multiply(cipherii.c1, r)
        c2 = bn.multiply(cipherii.c2, r)
        c3 = bn.pairing(tk.tk, cipherii.c1)
        c4 = cipherii.c3
        cipheri = CipherI(c1, c2, c3, c4)
        return cipheri

    def Test(self, cipher: Cipher, Tw: TrapKey, rk: ReKey):
        return (bn.pairing(Tw.tk, cipher.c1) == bn.pairing(cipher.c2, rk.rk))

    def Dec(self, cipher: Cipher, prikey: PriKey, hashtable: dict):
        if not isinstance(cipher, Cipher):
            raise TypeError("")
        m = None
        if isinstance(cipher, CipherII):
            sid = hashtable[self.hashfromCipherII(cipher)]
            m = (cipher.c3 / (bn.pairing(cipher.c2, self.g) ** sid)).coeffs[0]
        if isinstance(cipher, CipherI):
            div = self.modInverse(prikey.sk, bn.curve_order)
            m = (cipher.c4 / (cipher.c3 ** div)).coeffs[0]
        return self.decodeStr(int(m))

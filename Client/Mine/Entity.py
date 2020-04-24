from py_ecc import bn128 as bn


class PubKey:
    """ The format of public key"""

    def __init__(self, pk):
        if isinstance(pk, type(bn.G1)):
            self.pk = pk  # An element of G1 field
        else:
            raise TypeError("require G1 type for pk!")

    def __str__(self):
        return str(self.pk)


class PriKey:
    """ The format of private key"""

    def __init__(self, sk):
        if isinstance(sk, int):
            self.sk = sk  # An integer for G1 field
        else:
            raise TypeError("require int type for sk!")

    def __str__(self):
        return str(self.sk)


class Key:
    """ The format of user's key"""

    def __init__(self, prikey):
        if isinstance(prikey, PriKey):
            self.prikey = prikey
            pk = bn.multiply(bn.G1, self.prikey.sk)  # pk = g^sk
            self.pubkey = PubKey(pk)
        else:
            raise TypeError("require PubKey and PriKey type!")

    def __str__(self):
        return "===== pubkey =====\n" + str(self.pubkey) + "\n===== prikey =====\n" + str(self.prikey)


class TrapKey:
    """ The format of trapdoor """

    def __init__(self, tk):
        if isinstance(tk, type(bn.G2)):
            self.tk = tk
        else:
            raise TypeError("require G2 type for tk!")

    def __str__(self):
        return str(self.tk)


class ReKey:
    """ The format of rekey """

    def __init__(self, rk):
        if isinstance(rk, type(bn.G1)):
            self.rk = rk
        else:
            raise TypeError("require G1 type for rk!")

    def __str__(self):
        return str(self.rk)


class Token:
    """ The format of token"""

    def __init__(self, tk):
        if isinstance(tk, type(bn.G2)):
            self.tk = tk
        else:
            raise TypeError("require G2 type for tk!")

    def __str__(self):
        return "===== token =====\n" + "tk: " + str(self.tk)


class Cipher:
    """ The abstract of ciphertext """
    pass


class Srecord:
    """ The format of hash table element"""

    def __init__(self, sid, hc):
        if isinstance(sid, int) and isinstance(hc, int):
            self.sid = sid
            self.hc = hc
        else:
            raise TypeError("require int type for sid and int type for hc!")
    def __str__(self):
        return "===== Srecord =====\n" + "sid: " + str(self.sid) + "\nhc: " + str(
            self.hc)



class CipherII(Cipher):
    """ The format of second-level ciphertext """

    def __init__(self, c1, c2, c3):
        b1 = isinstance(c1, type(bn.G1))
        b2 = isinstance(c2, type(bn.G2))
        b3 = isinstance(c3, bn.FQ12)
        if b1 and b2 and b3:
            self.c1 = c1
            self.c2 = c2
            self.c3 = c3
        else:
            raise TypeError("require (G1,G2,FQ12) for second-level ciphertext!")

    def __str__(self):
        return "c1: " + str(self.c1) + "\nc2: " + str(self.c2) + "\nc3: " + str(self.c3)


class CipherI(Cipher):
    """ The format of first-level ciphertext """

    def __init__(self, c1, c2, c3, c4):
        b1 = isinstance(c1, type(bn.G1))
        b2 = isinstance(c2, type(bn.G2))
        b3 = isinstance(c3, bn.FQ12)
        b4 = isinstance(c4, bn.FQ12)
        if b1 and b2 and b3 and b4:
            self.c1 = c1
            self.c2 = c2
            self.c3 = c3
            self.c4 = c4
        else:
            raise TypeError("require (G1,G2,FQ12,FQ12) for second-level ciphertext!")

    def __str__(self):
        return "===== cipherI =====\n" + "c1: " + str(self.c1) + "\nc2: " + str(
            self.c2) + "\nc3: " + str(self.c3) + "\nc4: " + str(self.c4)

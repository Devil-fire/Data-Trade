from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import string
import random
import os
def keygen(method):
    if(method=='AES-128'):
        key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    elif(method=='AES-192'):
        key = ''.join(random.sample(string.ascii_letters + string.digits, 24))
    elif(method=='AES-256'):
        key = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    else:
        key='error'
    return key
def ivgen():
    return ''.join(random.sample(string.ascii_letters + string.digits, 16)).encode('utf-8')
def encrypt(data,key,iv):
    mode = AES.MODE_CFB
    cryptos = AES.new(key, mode, iv)
    cipher_data = cryptos.encrypt(data)
    return cipher_data

def decrypt(filename,key):
    f1=open(filename, 'rb')
    if os.path.exists('new'+filename[:]):
        os.remove('new'+filename[:])
    f2=open('new'+filename[:], 'ab')
    iv=f1.read(16)
    data=iv
    while (data):
        data=f1.read(83886080)#10M
        mode = AES.MODE_CFB
        cryptos = AES.new(key, mode, iv)
        plain_data = cryptos.decrypt(data)
        f2.write(plain_data)


if __name__ == '__main__':
    #key=keygen('AES-128')
    #encrypt('1.MP4',b'fOUKYXDQtdzcZn0k')
    decrypt('enc重走徐老院长初心路 社会实践视频.mp4',b'JUX02BtYLpPoO5QW')
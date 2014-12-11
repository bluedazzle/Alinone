#encoding:utf-8
from M2Crypto.EVP import Cipher
from M2Crypto import m2
from M2Crypto import util

ENCRYPT_OP = 1
DECRYPT_OP = 0

iv = '\0' * 16
PRIVATE_KEY = 'zhanjga156dghyt6e96f816db1d1huyj'

def Encrypt(data):
  cipher = Cipher(alg = 'aes_128_ecb', key = PRIVATE_KEY, iv = iv, op = ENCRYPT_OP)
  buf = cipher.update(data)
  buf = buf + cipher.final()
  del cipher
  # 将明文从字节流转为16进制
  output = ''
  for i in buf:
    output += '%02X' % (ord(i))
  return output

def Decrypt(data):
  # 将密文从16进制转为字节流
  data = util.h2b(data)
  cipher = Cipher(alg = 'aes_128_ecb', key = PRIVATE_KEY, iv = iv, op = DECRYPT_OP)
  buf = cipher.update(data)
  buf = buf + cipher.final()
  del cipher
  return buf


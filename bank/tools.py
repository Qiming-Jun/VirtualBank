import pymysql as MySQLdb
import datetime
import rsa
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def sqlconnect():
    db = MySQLdb.connect('localhost', 'root', '', 'bankdb', charset='utf8')
  #  cursor = db.cursor()
    return db

def DecodeDecrypt(ciphertext):
    file_path = os.path.abspath(__file__)
    file_path = "\\".join(file_path.split("\\")[:-1])

    private_path = open(file_path+"\\private_key.pem", 'r').read()
    private_key = RSA.import_key(private_path)

    text_decode = base64.b64decode(ciphertext)

    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key)
    return cipher_rsa_decrypt.decrypt(text_decode)
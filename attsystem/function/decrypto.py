# 解密数据
import re

from Crypto.Cipher import AES
import base64


def decrypto(text):
    print(text.decode())
    # 数据base64解码
    text = base64.b64decode(text.decode())
    # key 为云之家智能审批开发者选项提供的
    key = "G4JvA66QWMqwvQS7".encode('utf-8')
    mode = AES.MODE_ECB
    # 设置秘钥和加密模式
    cryptor = AES.new(key, mode)
    # 解密
    plain_text = cryptor.decrypt(text)
    # 还需处理末尾多符号的问题
    # print(plain_text)
    # return bytes.decode(plain_text).rstrip('\x01')
    return re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', str(plain_text, encoding='utf-8'))


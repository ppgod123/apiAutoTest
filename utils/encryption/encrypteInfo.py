#!/usr/bin/python 
# -*- coding: utf-8 -*-
import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from common.setting import ensure_path_sep

# 私钥路径
key_path = ensure_path_sep("\\Files\\keyDoc\\rsa.key")
# 公钥路径
pub_path = ensure_path_sep("\\Files\\keyDoc\\rsa.pub")


def create_key_pub():
    # 获取一个伪随机数生成器
    random_generator = Random.new().read
    # 获取一个rsa算法对应的密钥对生成器实例
    rsa = RSA.generate(1024, random_generator)

    # 生成私钥并保存
    private_pem = rsa.exportKey()
    with open(key_path, 'wb') as f:
        f.write(private_pem)

    # 生成公钥并保存
    public_pem = rsa.publickey().exportKey()
    with open(pub_path, 'wb') as f:
        f.write(public_pem)


def encrypt_info(message):
    with open(pub_path, 'r') as f:
        public_key = f.read()
        rsa_key_obj = RSA.importKey(public_key)
        cipher_obj = PKCS1_v1_5.new(rsa_key_obj)
        for k in message:
            cipher_text = base64.b64encode(cipher_obj.encrypt(k.encode()))
            print(cipher_text.decode())


if __name__ == "__main__":
    # 需要加密的内容
    message = ['12312312']
    encrypt_info(message)

#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-07-19

from Crypto.Cipher import AES;
from Crypto import Random;
import binascii;
import hmac, hashlib;

class cryptoLib:
    def __init__(self, encryptionKey, validationKey):
        self._encryptionKey = binascii.unhexlify(encryptionKey);
        self._validationKey = binascii.unhexlify(validationKey);

    def updateKeys(self, encryptionKey, validationKey):
        self._encryptionKey = binascii.unhexlify(encryptionKey);
        self._validationKey = binascii.unhexlify(validationKey);

    def encrypt(self, clearData):
        iv = Random.new().read(AES.block_size);
        cipher = AES.new(self._encryptionKey, AES.MODE_CBC, iv);
        clearData = str(clearData); #force a string
        padding = AES.block_size - (len(clearData) % AES.block_size)
        data = clearData + "".ljust(padding, chr(padding))
        data = cipher.encrypt(data)
        hashData = iv + data;
        #取16位
        hash = hmac.new(self._validationKey, hashData, hashlib.sha256).hexdigest() [:16];
        encryptData = binascii.hexlify(iv) + binascii.hexlify(data) + hash;
        return encryptData;

    def decrypt(self, encryptData):
        if not encryptData:
            return False;

        encryptData = binascii.unhexlify(encryptData)
        hash_size = 8
        validatHash = binascii.hexlify(encryptData[-hash_size:])

        localValiatData = encryptData [0:len(encryptData) - hash_size]
        localValiatHash = hmac.new(self._validationKey, localValiatData, hashlib.sha256).hexdigest() [:16]
        if (validatHash != localValiatHash):
            return False;

        iv = encryptData[:AES.block_size]
        cipher = AES.new(self._encryptionKey, AES.MODE_CBC, iv)
        data = encryptData[AES.block_size:][:len(encryptData) - AES.block_size - hash_size]
        data = cipher.decrypt(data)
        padding = ord(data[len(data) - 1])
        if padding > len(data):
            return False

        if data.count(chr(padding)) != padding:
            return False

        return data[:-padding]
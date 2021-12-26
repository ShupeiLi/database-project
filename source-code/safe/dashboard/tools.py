# -*- coding: utf-8 -*-

def encrypt(ono):
    dno = ""
    encrypt_dict = {"1":"5", "2":"3", "3":"7", "4":"9", "5":"0", 
                    "6":"1", "7":"8", "8":"2", "9":"4", "0":"6"}
    for i in range(len(ono)):
        dno = dno + encrypt_dict[ono[i]]
    return dno

def decrypt(dno):
    ono = ""
    decrypt_dict = {"1":"6", "2":"8", "3":"2", "4":"9", "5":"1",
                    "6":"0", "7":"3", "8":"7", "9":"4", "0":"5"}
    for i in range(len(dno)):
        ono = ono + decrypt_dict[dno[i]]
    return ono
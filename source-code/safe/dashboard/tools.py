# -*- coding: utf-8 -*-

def encrypt(ono):
    ono_str = str(ono)
    dno = ""
    encrypt_dict = {"1":"5", "2":"3", "3":"7", "4":"9", "5":"0", 
                    "6":"1", "7":"8", "8":"2", "9":"4", "0":"6"}
    for i in range(len(ono_str)):
        dno = dno + encrypt_dict[ono_str[i]]
    return int(dno)

def decrypt(dno):
    dno_str = str(dno)
    ono = ""
    decrypt_dict = {"1":"6", "2":"8", "3":"2", "4":"9", "5":"1",
                    "6":"0", "7":"3", "8":"7", "9":"4", "0":"5"}
    for i in range(len(dno_str)):
        ono = ono + decrypt_dict[dno_str[i]]
    return int(ono)
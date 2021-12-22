# -*- coding: utf-8 -*-

def encrypt(ono):
    ono_str = str(ono)
    dno = ""
    encrypt_dict = {"1":"5", "2":"3", "3":"7", "4":"9", "5":"0", 
                    "6":"1", "7":"8", "8":"2", "9":"4", "0":"6"}
    for i in range(len(ono_str)):
        dno = dno + encrypt_dict[ono_str[i]]
    return int(dno)
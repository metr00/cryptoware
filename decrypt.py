#!/usr/bin/env python3 
#
# this is the decryption script you need to run this script with
# the key in the same directory to unlock the files

import time 
import os 
from cryptography.fernet import Fernet

class ansi:
    RED = '\033[1;31m' 
    GREEN = '\033[1;32m' 
    BOLD = '\033[1m'
    CYAN = '\033[1;36m'
    END = '\033[0m'


def main():

    decrypting = False
    files = []
    count = 0

    
    #looping and parsing the files
    
    for file in os.listdir():
        
        if file == 'cryptoware.py':
            continue 
        elif file == 'thekey.key':
            print(f'{ansi.GREEN}[*]{ansi.END} key found')
            decrypting = True
            continue
        elif file == 'decrypt.py':
            continue
        elif os.path.isdir(file):
            continue
        files.append(file)
        count += 1

    
    #if key is found then decrypt
    
    if decrypting == True:


        with open('thekey.key', 'rb') as key:
            secretkey = key.read() 

        for file in files:
            with open(file, 'rb') as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(secretkey).decrypt(contents)
            with open(file, 'wb') as thefile:
                thefile.write(contents_decrypted)
            print(f'{ansi.CYAN}{file} files has been decrypted{ansi.END}')  
            file_original = os.path.splitext(file)[0]
            os.rename(file, file_original)

        print(f'{ansi.GREEN}[*]{ansi.END} {count} files has been decrypted')
        print(f'{ansi.GREEN}[*]{ansi.END} deleting key')
        os.remove('thekey.key')
        time.sleep(3)

    else:
        print(f'{ansi.RED}[!]{ansi.END} key not found exiting...')
        time.sleep(3)

if __name__ =="__main__":
    main()
